"""
Back simulation by extreme value theory to find alpha

TODO:
1.(DONE)fit by alpha
2.(DONE)apply to QQQ
3.(TODO)fit levy stable in scipy not genpareto

"""
from scipy.stats import genpareto
from scipy.optimize import minimize
from typing import Dict
import yfinance as yf
from curl_cffi import requests
import time
import numpy as np

def estimate_alpha_by_mle(excess_losses):
    alpha_est, loc_est, scale_est = genpareto.fit(excess_losses)
    return alpha_est, loc_est, scale_est

def get_ndx100_daily_returns(period) -> np.ndarray:
    """获取NDX100 (QQQ) 的日收益率数据"""
    session = requests.Session(impersonate="chrome")
    ticker = yf.Ticker("QQQ", session=session)
    hist = ticker.history(period=period)
    prices = hist['Close']
    daily_returns = prices.pct_change(1).dropna()
    return daily_returns.values
   
def test_estimate_alpha():
    true_alpha = 3.4
    simulated_price_change = genpareto.rvs(true_alpha, size=100000)
    estimated_alpha, loc, scale = estimate_alpha_by_mle(simulated_price_change)
    assert abs(estimated_alpha - true_alpha) < 0.05

def select_threshold(data: np.ndarray, percentile: float = 95.0) -> float:
    """选择尾部阈值，使用百分位数方法"""
    return np.percentile(np.abs(data), percentile)

def estimate_gpd_alpha_mle(data: np.ndarray, 
                          tail_type: str = "both",
                          threshold_percentile: float = 95.0) -> Dict:
    """
    使用MLE估计GPD的alpha参数
    
    Args:
        data: 日收益率数据
        tail_type: "upper", "lower", "both"
        threshold_percentile: 阈值百分位数
    
    Returns:
        包含alpha估计结果的字典
    """
    results = {}
    
    if tail_type in ["upper", "both"]:
        # 上尾分析（正收益）
        positive_returns = data[data > 0]
        if len(positive_returns) > 0:
            threshold = select_threshold(positive_returns, threshold_percentile)
            excesses = positive_returns[positive_returns > threshold] - threshold
            
            if len(excesses) > 10:  # 至少需要10个观测值
                try:
                    shape, loc, scale = genpareto.fit(excesses, floc=0)
                    alpha = 1.0 / shape if shape > 0 else np.inf
                    
                    results['upper_tail'] = {
                        'alpha': alpha,
                        'shape': shape,
                        'scale': scale,
                        'threshold': threshold,
                        'n_excesses': len(excesses),
                        'mean_excess': np.mean(excesses)
                    }
                except Exception as e:
                    results['upper_tail'] = {'error': str(e)}
    
    if tail_type in ["lower", "both"]:
        # 下尾分析（负收益的绝对值）
        negative_returns = np.abs(data[data < 0])
        if len(negative_returns) > 0:
            threshold = select_threshold(negative_returns, threshold_percentile)
            excesses = negative_returns[negative_returns > threshold] - threshold
            
            if len(excesses) > 10:
                try:
                    shape, loc, scale = genpareto.fit(excesses, floc=0)
                    alpha = 1.0 / shape if shape > 0 else np.inf
                    
                    results['lower_tail'] = {
                        'alpha': alpha,
                        'shape': shape,
                        'scale': scale,
                        'threshold': threshold,
                        'n_excesses': len(excesses),
                        'mean_excess': np.mean(excesses)
                    }
                except Exception as e:
                    results['lower_tail'] = {'error': str(e)}
    
    return results

def plot_gpd_fit(data: np.ndarray, results: Dict, tail: str = "upper"):
    """绘制GPD拟合效果图"""
    if tail not in results or 'error' in results[tail]:
        print(f"No valid results for {tail} tail")
        return
    
    tail_results = results[tail]
    threshold = tail_results['threshold']
    shape = tail_results['shape']
    scale = tail_results['scale']
    alpha = tail_results['alpha']
    
    # 准备数据
    if tail == "upper":
        relevant_data = data[data > 0]
        title = f"Upper Tail GPD Fit (α = {alpha:.2f})"
    else:
        relevant_data = np.abs(data[data < 0])
        title = f"Lower Tail GPD Fit (α = {alpha:.2f})"
    
    excesses = relevant_data[relevant_data > threshold] - threshold
    
    if len(excesses) == 0:
        return
        
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 1. 经验 vs 理论CDF
    sorted_excesses = np.sort(excesses)
    empirical_cdf = np.arange(1, len(sorted_excesses) + 1) / len(sorted_excesses)
    theoretical_cdf = genpareto.cdf(sorted_excesses, shape, scale=scale)
    
    ax1.plot(sorted_excesses, empirical_cdf, 'bo-', alpha=0.6, markersize=3, label='Empirical')
    ax1.plot(sorted_excesses, theoretical_cdf, 'r-', linewidth=2, label='GPD Theoretical')
    ax1.set_xlabel('Excess Loss')
    ax1.set_ylabel('CDF')
    ax1.set_title('CDF Comparison')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. 生存函数对数图
    survival_empirical = 1 - empirical_cdf
    survival_theoretical = 1 - theoretical_cdf
    
    ax2.loglog(sorted_excesses, survival_empirical, 'bo-', alpha=0.6, markersize=3, label='Empirical')
    ax2.loglog(sorted_excesses, survival_theoretical, 'r-', linewidth=2, label='GPD Theoretical')
    ax2.set_xlabel('Excess Loss')
    ax2.set_ylabel('Survival Probability')
    ax2.set_title('Log-Log Survival Plot')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    returns = get_ndx100_daily_returns(period="max")
    print(returns)
    threshold_percentile = 95
    plot_results = True
    # GPD拟合
    results = estimate_gpd_alpha_mle(returns, "both", threshold_percentile)
    
    # 输出结果
    print(f"\n=== GPD Alpha参数估计 (阈值: {threshold_percentile}%) ===")
    
    if 'upper_tail' in results and 'error' not in results['upper_tail']:
        upper = results['upper_tail']
        print(f"上尾 (正收益):")
        print(f"  Alpha: {upper['alpha']:.3f}")
        print(f"  Shape (ξ): {upper['shape']:.4f}")
        print(f"  Scale (σ): {upper['scale']:.4f}")
        print(f"  阈值: {upper['threshold']:.4f}")
        print(f"  超额观测数: {upper['n_excesses']}")
    
    if 'lower_tail' in results and 'error' not in results['lower_tail']:
        lower = results['lower_tail']
        print(f"下尾 (负收益):")
        print(f"  Alpha: {lower['alpha']:.3f}")
        print(f"  Shape (ξ): {lower['shape']:.4f}")
        print(f"  Scale (σ): {lower['scale']:.4f}")
        print(f"  阈值: {lower['threshold']:.4f}")
        print(f"  超额观测数: {lower['n_excesses']}")

    if plot_results:
        if 'upper_tail' in results:
            plot_gpd_fit(returns, results, "upper")
        if 'lower_tail' in results:
            plot_gpd_fit(returns, results, "lower")
    

    #estimated_alpha, loc, scale = estimate_alpha_by_mle(max_daily_price_change)
    #print(estimated_alpha)
    #test_estimate_alpha()