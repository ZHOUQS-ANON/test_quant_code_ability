"""生成 pandas 量化练习用的模拟日频行情数据。

数据完全由本地随机过程生成，不对应任何真实证券。
"""

from __future__ import annotations

import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "daily_bars.csv"
RANDOM_SEED = 20260508

ASSETS = [
    ("ALPHA", "Technology", 88.0, 0.00055, 0.016, 1.20),
    ("BETA", "Finance", 64.0, 0.00035, 0.012, 0.90),
    ("GAMMA", "Healthcare", 42.0, 0.00045, 0.014, 0.75),
    ("DELTA", "Energy", 55.0, 0.00025, 0.018, 1.05),
    ("OMEGA", "Consumer", 72.0, 0.00030, 0.013, 0.65),
    ("BENCH", "Benchmark", 100.0, 0.00030, 0.009, 1.00),
]
VOLUME_OFFSETS = {
    "ALPHA": 280_000,
    "BETA": 160_000,
    "GAMMA": 210_000,
    "DELTA": 130_000,
    "OMEGA": 190_000,
    "BENCH": 330_000,
}


def business_days(start: date, end: date) -> list[date]:
    days: list[date] = []
    current = start
    while current <= end:
        if current.weekday() < 5:
            days.append(current)
        current += timedelta(days=1)
    return days


def round_price(value: float) -> str:
    return f"{value:.2f}"


def main() -> None:
    random.seed(RANDOM_SEED)
    days = business_days(date(2023, 1, 3), date(2024, 12, 31))
    prices = {symbol: start for symbol, _, start, _, _, _ in ASSETS}
    rows: list[dict[str, str]] = []

    for i, day in enumerate(days):
        market_return = 0.0002 + 0.004 * math.sin(i / 23) + random.gauss(0, 0.006)

        for symbol, sector, _, drift, volatility, beta in ASSETS:
            seasonal = 0.002 * math.sin(i / 17 + len(symbol))
            asset_return = drift + beta * market_return + seasonal
            if symbol != "BENCH":
                asset_return += random.gauss(0, volatility)
            else:
                asset_return += random.gauss(0, volatility * 0.35)

            previous_close = prices[symbol]
            close = max(3.0, previous_close * (1.0 + asset_return))
            open_price = previous_close * (1.0 + random.gauss(0, volatility / 3))
            intraday_width = abs(random.gauss(volatility * 0.9, volatility / 4))
            high = max(open_price, close) * (1.0 + intraday_width)
            low = min(open_price, close) * (1.0 - intraday_width)
            volume_base = 1_000_000 + VOLUME_OFFSETS[symbol]
            volume = int(volume_base * (1.0 + abs(random.gauss(0, 0.35))))
            adj_close = close * (1.0 - 0.00003 * (i // 63))
            prices[symbol] = close

            row = {
                "date": day.isoformat(),
                "symbol": symbol,
                "sector": sector,
                "open": round_price(open_price),
                "high": round_price(high),
                "low": round_price(low),
                "close": round_price(close),
                "adj_close": round_price(adj_close),
                "volume": str(volume),
            }

            if day == date(2023, 6, 15) and symbol == "GAMMA":
                row["close"] = ""
            if day == date(2023, 9, 1) and symbol == "ALPHA":
                row["symbol"] = " ALPHA "

            rows.append(row)

    rows.append(rows[12].copy())
    random.shuffle(rows)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "date",
                "symbol",
                "sector",
                "open",
                "high",
                "low",
                "close",
                "adj_close",
                "volume",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
