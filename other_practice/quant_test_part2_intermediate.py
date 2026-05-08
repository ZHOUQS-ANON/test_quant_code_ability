"""
量化编程能力测试 - Part 2: 风险度量与投资组合 (40分)
请完成以下所有 TODO 题目。
测试时间建议: 40分钟
"""
import numpy as np
import pandas as pd

# ============================================================
# 数据准备（请勿修改）
# ============================================================
np.random.seed(123)
dates = pd.date_range("2020-01-01", "2025-12-31", freq="B")
n = len(dates)

returns_data = {
    "AAPL": np.random.normal(0.0008, 0.018, n),
    "GOOGL": np.random.normal(0.0006, 0.016, n),
    "TSLA": np.random.normal(0.0012, 0.035, n),
    "BRK-B": np.random.normal(0.0004, 0.012, n),
    "JPM": np.random.normal(0.0005, 0.020, n),
}
returns_df = pd.DataFrame(returns_data, index=dates)

# ============================================================
# 题目 4: VaR 与 CVaR (10分)
# ============================================================

# TODO 4.1 (4分): 用历史模拟法计算 95% 置信度的 Value at Risk (VaR)
# VaR(95%) = 收益率分布的第5百分位数（即最差的5%中的最好结果）
# 返回 daily VaR，以正数表示（如 0.03 表示每日 VaR 为 3%）
def historical_var(returns_df, confidence=0.95):
    """
    对每只股票计算 daily VaR，返回 Series
    注意: VaR 以正数表示损失的幅度
    """
    pass  # TODO

# TODO 4.2 (6分): 用历史模拟法计算 95% CVaR (Conditional VaR / Expected Shortfall)
# CVaR = 超过 VaR 阈值的那部分损失的平均值
def historical_cvar(returns_df, confidence=0.95):
    """
    对每只股票计算 daily CVaR，返回 Series
    """
    pass  # TODO

# ============================================================
# 题目 5: 投资组合构建 (18分)
# ============================================================

# TODO 5.1 (6分): 等权重组合 — 给定收益率，计算组合的日收益率序列
# 等权重 = 每只股票权重相同
def equal_weight_portfolio(returns_df):
    """
    返回组合日收益率 Series (index 与 returns_df 相同)
    """
    pass  # TODO

# TODO 5.2 (6分): 计算投资组合的 Sharpe Ratio
# Sharpe = (年化组合收益 - 无风险利率) / 年化组合波动率
# 无风险利率默认 3% (0.03)，一年 252 个交易日
def sharpe_ratio(portfolio_returns, risk_free_rate=0.03):
    """
    返回 Sharpe Ratio 浮点数
    """
    pass  # TODO

# TODO 5.3 (6分): 实现 Markowitz 最小方差组合
# 用 scipy.optimize.minimize 或解析解均可
# 目标: min w^T Σ w   subject to: sum(w) = 1, w_i >= 0
# 提示: 协方差矩阵用 returns_df.cov() * 252 年化
def minimum_variance_portfolio(returns_df):
    """
    返回最优权重 numpy array（顺序与 returns_df.columns 一致）
    暂不考虑无做空约束
    """
    pass  # TODO

# ============================================================
# 题目 6: 绩效归因 (12分)
# ============================================================

# TODO 6.1 (6分): 计算组合的累计收益率曲线（从 1 开始复利）
def cumulative_return_curve(returns_series):
    """
    输入: 日收益率 Series
    返回: 累计净值 Series (从 1.0 开始)
    """
    pass  # TODO

# TODO 6.2 (6分): 计算 Calmar Ratio = 年化收益率 / 最大回撤
def calmar_ratio(returns_series):
    """
    输入: 日收益率 Series
    返回: Calmar Ratio
    """
    pass  # TODO


if __name__ == "__main__":
    print("Part 2 测试文件加载成功，请完成所有 TODO 后运行 test_runner.py")
