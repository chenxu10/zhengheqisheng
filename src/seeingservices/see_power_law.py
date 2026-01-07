import numpy as np
from scipy.stats import uniform
import matplotlib.pyplot as plt

def uniform_sample_r(loc, scale, size):
    """生成均匀分布的随机数"""
    return uniform.rvs(loc=loc, scale=scale, size=size)

def generate_transformative_power_law_samples(alpha, x_min=1.0, size=1000):
    """使用变换方法生成幂律分布样本
    
    参数:
    alpha: 幂律指数 (应该 > 1)
    x_min: 分布的下限
    size: 样本数量
    
    返回:
    幂律分布的样本数组
    """
    uniform_r = uniform_sample_r(0, 1, size)
    
    if alpha <= 1:
        raise ValueError("alpha 必须大于 1，否则分布无法归一化")
    
    power_law_samples = x_min * np.power(1.0 - uniform_r, -1.0/(alpha - 1))
    
    return power_law_samples

def create_log_space_bins(x_min, samples) -> np.ndarray:
    """
    Creates an array of numbers that are evenly distrbuted on log space
    """
    bins = np.logspace(np.log10(x_min), np.log10(np.max(samples)), 100)
    return bins

def plot_linear_histogram(samples, ax=None):
    """
    Plot linear scale histogram of power-law samples

    参数:
    samples: Power-law distributed samples
    ax: Matplotlib axes object. If None, uses current axes

    返回:
    ax: The axes object used for plotting
    """

    if ax is None:
        ax = plt.gca()

    ax.hist(samples, bins=100, density=True, alpha=0.7, color='blue')
    ax.set_xlabel('x')
    ax.set_ylabel('Probability density')
    ax.set_title('Power-law distribution (linear scale)')
    ax.grid(True, alpha=0.3)

    return ax

def plot_loglog_histogram(samples, x_min, ax=None):
    """
    Plot log-log scale histogram of power-law samples

    参数:
    samples: Power-law distributed samples
    x_min: Minimum value of the distribution
    ax: Matplotlib axes object. If None, uses current axes

    返回:
    ax: The axes object used for plotting
    hist: Histogram values
    bin_centers: Bin center values
    """

    if ax is None:
        ax = plt.gca()

    bins = np.linspace(x_min, np.max(samples), 100)
    hist, bin_edges = np.histogram(samples, bins=bins, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Plot only positive histogram values
    ax.loglog(bin_centers[hist > 0], hist[hist > 0], 'o-', alpha=0.7)
    ax.set_xlabel('x (log scale)')
    ax.set_ylabel('Probability density (log scale)')
    ax.set_title('Power-law distribution (log-log scale)')
    ax.grid(True, alpha=0.3, which='both')

    return ax, hist, bin_centers

def plot_loglog_histogram_log_binning(samples, x_min, ax=None):
    """
    Plot log-log scale histogram with proper log binning method

    This method produces cleaner plots like Newman's plot (c) by:
    - Using manual density normalization by bin width
    - Using geometric mean for bin centers (correct for log scale)
    - Reducing noise in the tail region

    参数:
    samples: Power-law distributed samples
    x_min: Minimum value of the distribution
    ax: Matplotlib axes object. If None, uses current axes

    返回:
    ax: The axes object used for plotting
    density: Density values
    bin_centers: Bin center values
    """
    import matplotlib.pyplot as plt

    if ax is None:
        ax = plt.gca()

    # Create log-spaced bins
    bins = create_log_space_bins(x_min, samples)

    # Get counts without automatic density normalization
    counts, bin_edges = np.histogram(samples, bins=bins, density=False)

    # Manual density normalization by bin width
    bin_widths = bin_edges[1:] - bin_edges[:-1]
    density = counts / (bin_widths * len(samples))

    # Use geometric mean for bin centers (correct for log-scale bins)
    bin_centers = np.sqrt(bin_edges[:-1] * bin_edges[1:])

    # Plot only bins with positive counts
    mask = counts > 0
    ax.loglog(bin_centers[mask], density[mask], 'o-', alpha=0.7)
    ax.set_xlabel('x (log scale)')
    ax.set_ylabel('Probability density (log scale)')
    ax.set_title('Power-law distribution with log binning')
    ax.grid(True, alpha=0.3, which='both')

    return ax, density, bin_centers

def calculate_sample_statistics(samples, x_min):
    """
    Calculate statistical metrics for power-law samples

    参数:
    samples: Power-law distributed samples
    x_min: Expected minimum value of the distribution

    返回:
    dict: Dictionary containing statistical metrics
    """
    return {
        'count': len(samples),
        'min': np.min(samples),
        'max': np.max(samples),
        'median': np.median(samples),
        'mean': np.mean(samples),
        'x_min': x_min
    }

def print_sample_statistics(stats):
    """
    Print formatted statistical metrics for power-law samples

    参数:
    stats: Dictionary containing statistical metrics from calculate_sample_statistics
    """
    print(f"生成的样本统计:")
    print(f"  样本数: {stats['count']}")
    print(f"  最小值: {stats['min']:.4f} (应该接近 x_min={stats['x_min']})")
    print(f"  最大值: {stats['max']:.4f}")
    print(f"  中位数: {stats['median']:.4f}")
    print(f"  均值: {stats['mean']:.4f}")




# 测试代码
if __name__ == "__main__":
    alpha = 2.5  # 幂律指数
    x_min = 1.0  # 下限
    samples = generate_transformative_power_law_samples(alpha, x_min, 100000)

    # 绘制直方图
    fig = plt.figure(figsize=(10, 6))

    # 使用对数坐标显示幂律分布的特征
    ax1 = plt.subplot(2, 2, 1)
    plot_linear_histogram(samples, ax=ax1)

    ax2 = plt.subplot(2, 2, 2)
    plot_loglog_histogram(samples, x_min, ax=ax2)

    ax3 = plt.subplot(2, 2, 3)
    plot_loglog_histogram_log_binning(samples, x_min, ax=ax3)

    plt.tight_layout()
    plt.show()

    stats = calculate_sample_statistics(samples, x_min)
    print_sample_statistics(stats)