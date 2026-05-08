"""
量化编程能力测试 - Part 1: 基础数据处理 (30分)
请完成以下所有 TODO 题目。
测试时间建议: 30分钟
"""
import numpy as np
import pandas as pd

# ============================================================
# 数据准备（请勿修改）
# ============================================================
np.random.seed(42)
dates = pd.date_range("2020-01-01", "2025-12-31", freq="B")  # 交易日
n = len(dates)

# 模拟 4 只股票的日收益率数据
returns_data = {
    "AAPL": np.random.normal(0.0008, 0.018, n),
    "GOOGL": np.random.normal(0.0006, 0.016, n),
    "TSLA": np.random.normal(0.0012, 0.035, n),
    "BRK-B": np.random.normal(0.0004, 0.012, n),
}
price_df = pd.DataFrame(returns_data, index=dates)

# 模拟日度因子数据
factor_data = {
    "Mkt-RF": np.random.normal(0.0003, 0.012, n),
    "SMB": np.random.normal(0.0001, 0.008, n),
    "HML": np.random.normal(0.0002, 0.009, n),
}
factor_df = pd.DataFrame(factor_data, index=dates)

# ============================================================
# 题目 1: 数据清洗与检查 (8分)
# ============================================================

# TODO 1.1 (2分): 检查 price_df 中每只股票有多少个缺失值 (NaN)
# 提示: 用 isnull() + sum()
def count_missing(df):
    """返回每列的缺失值数量 Series"""
    pass  # TODO

# TODO 1.2 (2分): 检查 price_df 的 index 是否是单调递增的唯一 DatetimeIndex
# 提示: 用 index.is_monotonic_increasing 和 index.is_unique
def check_index_quality(df):
    """返回 (是否单调递增, 是否唯一)"""
    pass  # TODO

# TODO 1.3 (4分): 将日收益率转换为价格序列（从 100 开始），并计算每只股票的
# 累计最大回撤 (Maximum Drawdown)
# 公式: MDD = (Peak - Trough) / Peak，即从最高点到之后最低点的最大跌幅
def compute_max_drawdown(returns_df):
    """
    输入: 日收益率 DataFrame
    返回: 每只股票的最大回撤 Series (值为正数，如 0.35 表示 35% 回撤)
    """
    pass  # TODO

# ============================================================
# 题目 2: 统计分析与因子暴露 (12分)
# ============================================================

# TODO 2.1 (4分): 计算每只股票的年化收益率和年化波动率
# 假设一年有 252 个交易日
def annualized_stats(returns_df):
    """
    返回 DataFrame，index 为股票代码，columns 为 ['annual_return', 'annual_vol']
    annual_return = 日均收益率 * 252
    annual_vol = 日收益率标准差 * sqrt(252)
    """
    pass  # TODO

# TODO 2.2 (4分): 计算每只股票与市场因子 (Mkt-RF) 的 Beta
# Beta = Cov(stock_return, market_return) / Var(market_return)
def compute_beta(returns_df, market_returns):
    """
    返回每只股票的 Beta Series
    """
    pass  # TODO

# TODO 2.3 (4分): 对每只股票跑一元线性回归 against Mkt-RF，返回 Alpha 和 Beta
# 使用 np.polyfit 或手动计算
# Alpha = mean(stock_return) - Beta * mean(market_return)
def compute_alpha_beta(returns_df, market_returns):
    """
    返回 DataFrame，index 为股票代码，columns 为 ['alpha', 'beta']
    alpha 需要年化（日 alpha * 252）
    """
    pass  # TODO

# ============================================================
# 题目 3: 相关性分析 (10分)
# ============================================================

# TODO 3.1 (4分): 计算收益率的相关性矩阵，并找出与 AAPL 相关性最高的股票
def find_most_correlated(returns_df, target="AAPL"):
    """
    返回 (相关性最高的股票代码, 相关系数)
    不包括 target 自身
    """
    pass  # TODO

# TODO 3.2 (6分): 计算滚动 60 日相关性（AAPL vs GOOGL），返回一个 Series
# 提示: 用 rolling() + corr 或 rolling().apply()
def rolling_correlation(returns_df, stock1="AAPL", stock2="GOOGL", window=60):
    """
    返回 rolling correlation Series
    """
    pass  # TODO


if __name__ == "__main__":
    print("Part 1 测试文件加载成功，请完成所有 TODO 后运行 test_runner.py")
