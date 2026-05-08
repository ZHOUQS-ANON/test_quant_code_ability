"""练习合约测试。

默认测试参考答案：

    pytest

完成 TODO 后测试自己的实现：

    QUANT_MODULE=exercises.quant_project pytest
"""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd


MODULE_NAME = os.getenv("QUANT_MODULE", "solutions.reference_solution")
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

q = importlib.import_module(MODULE_NAME)
DATA_PATH = ROOT / "data" / "daily_bars.csv"


def test_load_price_data_cleans_daily_bars() -> None:
    df = q.load_price_data(DATA_PATH)

    assert not df.empty
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert df[["date", "symbol"]].duplicated().sum() == 0
    assert df["symbol"].str.startswith(" ").sum() == 0
    assert df["symbol"].str.endswith(" ").sum() == 0
    assert df["close"].isna().sum() == 0


def test_make_wide_prices_and_returns() -> None:
    df = q.load_price_data(DATA_PATH)
    prices = q.make_wide_prices(df)
    returns = q.calculate_returns(prices)

    assert prices.index.is_monotonic_increasing
    assert {"ALPHA", "BETA", "GAMMA", "DELTA", "OMEGA", "BENCH"} <= set(prices.columns)
    assert prices.shape == returns.shape
    assert returns.iloc[1:].notna().all().all()


def test_add_technical_features_is_grouped_by_symbol() -> None:
    df = q.load_price_data(DATA_PATH)
    featured = q.add_technical_features(df)

    expected_columns = {
        "daily_return",
        "ma_5",
        "ma_20",
        "volatility_20",
        "dollar_volume",
    }
    assert expected_columns <= set(featured.columns)

    alpha = featured[featured["symbol"] == "ALPHA"].sort_values("date")
    manual_ma_5 = alpha["adj_close"].rolling(5).mean()
    pd.testing.assert_series_equal(
        alpha["ma_5"].reset_index(drop=True),
        manual_ma_5.reset_index(drop=True),
        check_names=False,
    )


def test_signal_backtest_and_performance_summary() -> None:
    df = q.load_price_data(DATA_PATH)
    prices = q.make_wide_prices(df)
    signal = q.build_monthly_momentum_signal(prices, lookback=60, top_n=2)
    returns = q.backtest_long_only_momentum(prices, lookback=60, top_n=2)
    summary = q.summarize_performance(returns)

    assert not signal.empty
    assert "BENCH" not in signal.columns
    row_sums = signal.sum(axis=1)
    assert row_sums.between(0.0, 1.0).all()
    assert np.isclose(row_sums, 1.0).any()
    assert returns.index.equals(prices.index)
    assert returns.name == "momentum_strategy"
    assert {
        "total_return",
        "annual_return",
        "annual_volatility",
        "sharpe",
        "max_drawdown",
        "win_rate",
    } <= set(summary.index)
    assert summary["max_drawdown"] <= 0
    assert 0 <= summary["win_rate"] <= 1
