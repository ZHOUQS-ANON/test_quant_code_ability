"""
量化编程能力测试 - Part 3: 时间序列与高级建模 (30分)
请完成以下所有 TODO 题目。
测试时间建议: 40分钟
"""
import numpy as np
import pandas as pd

# ============================================================
# 数据准备（请勿修改）
# ============================================================
np.random.seed(456)
dates = pd.date_range("2020-01-01", "2025-12-31", freq="B")
n = len(dates)

# 模拟有自相关特征的股票收益率（AR(1) 过程）
def generate_ar1(n, phi, mu, sigma):
    """生成 AR(1) 序列"""
    eps = np.random.normal(0, sigma, n)
    r = np.zeros(n)
    r[0] = mu + eps[0]
    for t in range(1, n):
        r[t] = mu + phi * (r[t-1] - mu) + eps[t]
    return r

returns_data = {
    "Stock_A": generate_ar1(n, phi=0.1, mu=0.0005, sigma=0.015),
    "Stock_B": generate_ar1(n, phi=-0.05, mu=0.0003, sigma=0.018),
    "Stock_C": generate_ar1(n, phi=0.0, mu=0.0008, sigma=0.022),
}
returns_df = pd.DataFrame(returns_data, index=dates)

# 模拟价格数据（已知价格）
price_data = {
    "Stock_A": 100 * np.cumprod(1 + returns_data["Stock_A"]),
    "Stock_B": 100 * np.cumprod(1 + returns_data["Stock_B"]),
    "Stock_C": 100 * np.cumprod(1 + returns_data["Stock_C"]),
}
price_df = pd.DataFrame(price_data, index=dates)

# ============================================================
# 题目 7: 时间序列特征 (12分)
# ============================================================

# TODO 7.1 (4分): 计算每只股票收益率的一阶自相关系数 (lag-1 autocorrelation)
# 提示: 用 pd.Series.autocorr(lag=1) 或手动 shift 计算
def compute_autocorrelation(returns_df, lag=1):
    """
    返回每只股票的 lag-1 自相关系数 Series
    """
    pass  # TODO

# TODO 7.2 (4分): 计算每只股票的 20 日滚动波动率，并找出波动率最高的日期
# 用 rolling().std()
def max_rolling_volatility_date(returns_df, window=20):
    """
    对每只股票找出 20 日滚动波动率最大的交易日
    返回 DataFrame, index=股票代码, columns=['max_vol', 'date']
    """
    pass  # TODO

# TODO 7.3 (4分): 实现简单的布林带 (Bollinger Bands)
# 中轨 = 20日移动均线，上轨 = 中轨 + 2*标准差，下轨 = 中轨 - 2*标准差
# 计算每只股票价格突破上轨的天数占比
def bollinger_breakout_ratio(price_df, window=20, num_std=2):
    """
    返回每只股票价格超过上轨的天数占比 Series
    """
    pass  # TODO

# ============================================================
# 题目 8: 回测框架基础 (10分)
# ============================================================

# TODO 8.1 (10分): 实现一个简单的移动平均交叉策略回测
# 策略规则:
#   - 当短期均线 > 长期均线时，全仓持有（信号 = 1）
#   - 当短期均线 <= 长期均线时，空仓（信号 = 0）
#   - 交易有 1 天延迟（用前一天的信号交易今天的收益率）
#   - 不考虑交易成本，初始资金 = 1.0
def moving_average_crossover_backtest(price_series, short_window=20, long_window=50):
    """
    输入: 单只股票的价格 Series
    返回: dict，包含:
        - 'cumulative_return': 策略累计净值 Series
        - 'total_return': 总收益率 (float)
        - 'sharpe_ratio': 年化 Sharpe Ratio (float, 无风险利率=0)
        - 'max_drawdown': 最大回撤 (float, 正数)
        - 'win_rate': 策略信号正确的天数占比 (持仓时收益为正的天数/持仓总天数)
    """
    pass  # TODO

# ============================================================
# 题目 9: 因子分析 (8分)
# ============================================================

# 重新生成因子数据
np.random.seed(789)
factor_df = pd.DataFrame({
    "Mkt-RF": np.random.normal(0.0003, 0.012, n),
    "SMB": np.random.normal(0.0001, 0.008, n),
    "HML": np.random.normal(0.0002, 0.009, n),
}, index=dates)

# TODO 9.1 (8分): 对 Stock_A 做 Fama-French 三因子回归
# R_stock - Rf = alpha + beta_mkt * Mkt-RF + beta_smb * SMB + beta_hml * HML + epsilon
# 用 np.linalg.lstsq 求解
# 假设 Rf = 0 (简化)
def fama_french_regression(stock_returns, factor_df):
    """
    输入:
        stock_returns: 某只股票的日收益率 Series
        factor_df: 三因子 DataFrame (Mkt-RF, SMB, HML)
    返回: dict，包含:
        - 'alpha': 年化 alpha (float)
        - 'betas': numpy array [beta_mkt, beta_smb, beta_hml]
        - 'r_squared': R² (float)
        - 'residual_std': 残差标准差 (float)
    """
    pass  # TODO


if __name__ == "__main__":
    print("Part 3 测试文件加载成功，请完成所有 TODO 后运行 test_runner.py")
