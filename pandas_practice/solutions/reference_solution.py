"""参考答案：pandas 量化练习完整实现。"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "daily_bars.csv"
NUMERIC_COLUMNS = ["open", "high", "low", "close", "adj_close", "volume"]


def resample_month_end(frame: pd.DataFrame) -> pd.DataFrame:
    """兼容 pandas 新旧版本的月末重采样。"""
    try:
        return frame.resample("ME").last()
    except ValueError:
        return frame.resample("M").last()


def load_price_data(path: str | Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    df["symbol"] = df["symbol"].astype(str).str.strip()
    df["sector"] = df["sector"].astype(str).str.strip()

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["close"] = df["close"].fillna(df["adj_close"])
    df = df.dropna(subset=["date", "symbol", "adj_close"])
    df = df.drop_duplicates(subset=["date", "symbol"], keep="last")
    df = df.sort_values(["symbol", "date"]).reset_index(drop=True)
    return df


def make_wide_prices(df: pd.DataFrame, price_col: str = "adj_close") -> pd.DataFrame:
    prices = df.pivot(index="date", columns="symbol", values=price_col)
    return prices.sort_index()


def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change()


def add_technical_features(df: pd.DataFrame) -> pd.DataFrame:
    featured = df.sort_values(["symbol", "date"]).copy()
    grouped = featured.groupby("symbol", group_keys=False)

    featured["daily_return"] = grouped["adj_close"].pct_change()
    featured["ma_5"] = grouped["adj_close"].transform(lambda s: s.rolling(5).mean())
    featured["ma_20"] = grouped["adj_close"].transform(lambda s: s.rolling(20).mean())
    featured["volatility_20"] = grouped["daily_return"].transform(
        lambda s: s.rolling(20).std()
    )
    featured["dollar_volume"] = featured["close"] * featured["volume"]
    return featured


def build_monthly_momentum_signal(
    prices: pd.DataFrame,
    lookback: int = 60,
    top_n: int = 2,
    benchmark_symbol: str = "BENCH",
) -> pd.DataFrame:
    asset_prices = prices.drop(columns=[benchmark_symbol], errors="ignore")
    momentum = resample_month_end(asset_prices.pct_change(lookback))

    weights = pd.DataFrame(0.0, index=momentum.index, columns=asset_prices.columns)
    for date, row in momentum.iterrows():
        winners = row.dropna().nlargest(top_n).index
        if len(winners) > 0:
            weights.loc[date, winners] = 1.0 / len(winners)

    return weights


def backtest_long_only_momentum(
    prices: pd.DataFrame,
    lookback: int = 60,
    top_n: int = 2,
    benchmark_symbol: str = "BENCH",
) -> pd.Series:
    asset_prices = prices.drop(columns=[benchmark_symbol], errors="ignore")
    daily_returns = asset_prices.pct_change()
    monthly_weights = build_monthly_momentum_signal(
        prices,
        lookback=lookback,
        top_n=top_n,
        benchmark_symbol=benchmark_symbol,
    )

    aligned_index = daily_returns.index.union(monthly_weights.index).sort_values()
    daily_weights = (
        monthly_weights.reindex(aligned_index)
        .ffill()
        .reindex(daily_returns.index)
        .shift(1)
        .fillna(0.0)
    )

    strategy_returns = (daily_weights * daily_returns).sum(axis=1)
    strategy_returns.name = "momentum_strategy"
    return strategy_returns.fillna(0.0)


def summarize_performance(
    returns: pd.Series,
    periods_per_year: int = 252,
    risk_free_rate: float = 0.0,
) -> pd.Series:
    returns = returns.dropna()
    if returns.empty:
        raise ValueError("returns 不能为空")

    equity = (1.0 + returns).cumprod()
    total_return = equity.iloc[-1] - 1.0
    annual_return = equity.iloc[-1] ** (periods_per_year / len(returns)) - 1.0
    annual_volatility = returns.std() * np.sqrt(periods_per_year)
    excess_daily = returns - risk_free_rate / periods_per_year
    sharpe = np.nan
    if excess_daily.std() != 0:
        sharpe = excess_daily.mean() / excess_daily.std() * np.sqrt(periods_per_year)

    drawdown = equity / equity.cummax() - 1.0
    max_drawdown = drawdown.min()
    win_rate = (returns > 0).mean()

    return pd.Series(
        {
            "total_return": total_return,
            "annual_return": annual_return,
            "annual_volatility": annual_volatility,
            "sharpe": sharpe,
            "max_drawdown": max_drawdown,
            "win_rate": win_rate,
        }
    )


def main() -> None:
    df = load_price_data()
    prices = make_wide_prices(df)
    featured = add_technical_features(df)
    strategy_returns = backtest_long_only_momentum(prices)
    benchmark_returns = prices["BENCH"].pct_change().fillna(0.0)

    result = pd.DataFrame(
        {
            "momentum_strategy": summarize_performance(strategy_returns),
            "benchmark": summarize_performance(benchmark_returns),
        }
    )

    print("行情数据 shape:", df.shape)
    print("特征数据 shape:", featured.shape)
    print("价格矩阵 shape:", prices.shape)
    print(result.round(4))


if __name__ == "__main__":
    main()
