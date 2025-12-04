import numpy as np
from scipy.optimize import minimize

def power_law_pdf(x, alpha, xmin):
    C = (alpha - 1) * xmin **(alpha - 1)
    return C * x ** (- alpha)


class PowerLawEstimator:
    def __init__(self, data, threshold_quantile):
        self.data = data
        self.threshold_quantile = threshold_quantile

    def extract_tail(self, returns, side='right'):
        """
        提取尾部数据
        
        Parameters:
        -----------
        returns : array-like
            收益率序列
        side : str
            'right' 表示右尾（正收益率极端值）
            'left' 表示左尾（负收益率极端值，取绝对值）
        
        Returns:
        --------
        tail_data : numpy array
            尾部数据
        """
        returns = np.array(returns)
        
        if side == 'right':
            # 右尾：正收益率
            positive_returns = returns[returns > 0]
            self.threshold = np.quantile(positive_returns, self.threshold_quantile)
            self.tail_data = positive_returns[positive_returns >= self.threshold] - self.threshold
        else:
            # 左尾：负收益率取绝对值
            negative_returns = -returns[returns < 0]
            self.threshold = np.quantile(negative_returns, self.threshold_quantile)
            self.tail_data = negative_returns[negative_returns >= self.threshold] - self.threshold
        
        print(f"尾部数据提取 ({side}尾):")
        print(f"  阈值: {self.threshold:.6f}")
        print(f"  尾部观测数: {len(self.tail_data)}")
        print(f"  占总数比例: {len(self.tail_data)/len(returns):.2%}")
        
        return self.tail_data

    def pareto_log_likelihood(self, alpha, data):
        """
        帕累托分布对数似然函数
        
        帕累托分布PDF: f(x) = α * x_m^α / x^(α+1)
        对于超出阈值的数据: x = threshold + excess
        """
        if alpha <= 0:
            return 1e10  # 惩罚非正alpha
        
        n = len(data)
        # 帕累托分布的对数似然（忽略常数项）
        ll = n * np.log(alpha) - (alpha + 1) * np.sum(np.log(1 + data/self.threshold))
        return -ll  # 返回负对数似然用于最小化

    def estimate_alpha(self, returns, side='right'):
        """
        估计帕累托分布的尾部指数α
        
        Returns:
        --------
        alpha : float
            估计的尾部指数
        """
        # 提取尾部数据
        tail_data = self.extract_tail(returns, side)
        
        if len(tail_data) < 10:
            raise ValueError("尾部数据太少，无法进行可靠估计")
        
        # 初始猜测值
        initial_alpha = 2.0
        
        # 使用最大似然估计
        result = minimize(
            self.pareto_log_likelihood,
            initial_alpha,
            args=(tail_data,),
            bounds=[(0.1, 10)],  # alpha必须为正
            method='L-BFGS-B'
        )
        
        if result.success:
            self.alpha = result.x[0]
            
            # 计算标准误差（使用Fisher信息）
            n = len(tail_data)
            self.alpha_std = self.alpha / np.sqrt(n)
            
            print(f"\n最大似然估计结果:")
            print(f"  α估计值: {self.alpha:.4f}")
            print(f"  标准误差: {self.alpha_std:.4f}")
            print(f"  95%置信区间: [{self.alpha - 1.96*self.alpha_std:.4f}, "
                  f"{self.alpha + 1.96*self.alpha_std:.4f}]")
            
            return self.alpha
        else:
            raise RuntimeError(f"优化失败: {result.message}")