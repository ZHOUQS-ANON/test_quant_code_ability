"""TODO 版：用 pandas 完成一个迷你量化项目。

按 exercises/01_quant_project.md 的说明补全每个函数。
完成后运行：

    QUANT_MODULE=exercises.quant_project pytest
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "daily_bars.csv"


def load_price_data(path: str | Path = DATA_PATH) -> pd.DataFrame:
    """加载并清洗日频行情长表。

    返回字段至少包含：
    date, symbol, sector, open, high, low, close, adj_close, volume
    """
    raise NotImplementedError("请完成任务 1：加载并清洗数据")


def make_wide_prices(df: pd.DataFrame, price_col: str = "adj_close") -> pd.DataFrame:
    """把长表行情转为 date x symbol 的价格矩阵。"""
    raise NotImplementedError("请完成任务 2：构建价格宽表")


def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """计算日收益率矩阵。"""
    raise NotImplementedError("请完成任务 3：计算收益率")


def add_technical_features(df: pd.DataFrame) -> pd.DataFrame:
    """在长表上增加日收益、均线、波动率和成交额特征。"""
    raise NotImplementedError("请完成任务 4：生成技术特征")


def build_monthly_momentum_signal(
    prices: pd.DataFrame,
    lookback: int = 60,
    top_n: int = 2,
    benchmark_symbol: str = "BENCH",
) -> pd.DataFrame:
    """构建月度动量等权持仓表。"""
    raise NotImplementedError("请完成任务 5：动量信号")


def backtest_long_only_momentum(
    prices: pd.DataFrame,
    lookback: int = 60,
    top_n: int = 2,
    benchmark_symbol: str = "BENCH",
) -> pd.Series:
    """回测月度调仓的多头动量策略，返回日收益率序列。"""
    raise NotImplementedError("请完成任务 6：策略回测")


def summarize_performance(
    returns: pd.Series,
    periods_per_year: int = 252,
    risk_free_rate: float = 0.0,
) -> pd.Series:
    """汇总策略绩效指标。"""
    raise NotImplementedError("请完成任务 6：绩效评估")


def main() -> None:
    df = load_price_data()
    prices = make_wide_prices(df)
    featured = add_technical_features(df)
    strategy_returns = backtest_long_only_momentum(prices)
    summary = summarize_performance(strategy_returns)

    print("行情数据：", df.shape)
    print("特征数据：", featured.shape)
    print("价格矩阵：", prices.shape)
    print(summary.round(4))


if __name__ == "__main__":
    main()
