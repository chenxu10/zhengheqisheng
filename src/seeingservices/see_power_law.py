import numpy as np
from scipy.stats import uniform

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
    # 生成均匀分布的随机数
    uniform_r = uniform_sample_r(0, 1, size)
    
    # 使用正确的变换公式
    # 公式: x = x_min * (1-r)^{-1/(alpha-1)}
    # 注意: alpha 必须大于 1
    if alpha <= 1:
        raise ValueError("alpha 必须大于 1，否则分布无法归一化")
    
    # 使用向量化操作提高效率
    power_law_samples = x_min * np.power(1.0 - uniform_r, -1.0/(alpha - 1))
    
    return power_law_samples

# 测试代码
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    # 生成样本
    alpha = 2.5  # 幂律指数
    x_min = 1.0  # 下限
    samples = generate_transformative_power_law_samples(alpha, x_min, 10000)
    
    # 绘制直方图
    plt.figure(figsize=(10, 6))
    
    # 使用对数坐标显示幂律分布的特征
    plt.subplot(1, 2, 1)
    plt.hist(samples, bins=100, density=True, alpha=0.7, color='blue')
    plt.xlabel('x')
    plt.ylabel('Probability density')
    plt.title('Power-law distribution (linear scale)')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    # 对数对数坐标图，幂律分布应该显示为直线
    hist, bin_edges = np.histogram(samples, bins=np.logspace(np.log10(x_min), 
                                                            np.log10(np.max(samples)), 
                                                            50), density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    plt.loglog(bin_centers[hist > 0], hist[hist > 0], 'o-', alpha=0.7)
    plt.xlabel('x (log scale)')
    plt.ylabel('Probability density (log scale)')
    plt.title('Power-law distribution (log-log scale)')
    plt.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.show()
    
    # 打印统计信息
    print(f"生成的样本统计:")
    print(f"  样本数: {len(samples)}")
    print(f"  最小值: {np.min(samples):.4f} (应该接近 x_min={x_min})")
    print(f"  最大值: {np.max(samples):.4f}")
    print(f"  中位数: {np.median(samples):.4f}")
    print(f"  均值: {np.mean(samples):.4f}")