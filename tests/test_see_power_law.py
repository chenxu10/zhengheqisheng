import numpy as np
from scipy.stats import uniform
import pytest
import matplotlib.pyplot as plt
from src.seeingservices import see_power_law as spl

def test_uniform_sample_r():
    loc = 0
    scale = 1
    size = 100000
    samples = spl.uniform_sample_r(loc, scale, size)

    assert len(samples) == size
    assert np.min(samples) == pytest.approx(0, abs=1e-4)

def test_generate_transformative_power_law_samples():
    """使用变换方法生成幂律分布样本
    
    参数:
    alpha: 幂律指数 (应该 > 1)
    x_min: 分布的下限
    size: 样本数量
    
    返回:
    幂律分布的样本数组
    """
    alpha = 2.5
    size = 10000
    x_min = 1
    samples = spl.generate_transformative_power_law_samples(alpha, x_min, size)
    
    assert len(samples) == size
    assert np.min(samples) == pytest.approx(1, abs=1e-3)
