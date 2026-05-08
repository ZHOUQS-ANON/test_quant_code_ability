"""
量化编程能力测试 - 自动评分系统
运行方式: python test_runner.py
"""
import numpy as np
import pandas as pd
from collections import OrderedDict

# ============================================================
# 生成测试数据
# ============================================================
np.random.seed(42)
dates = pd.date_range("2020-01-01", "2025-12-31", freq="B")
n = len(dates)

returns_data_4 = {
    "AAPL": np.random.normal(0.0008, 0.018, n),
    "GOOGL": np.random.normal(0.0006, 0.016, n),
    "TSLA": np.random.normal(0.0012, 0.035, n),
    "BRK-B": np.random.normal(0.0004, 0.012, n),
}

def make_data_4():
    return pd.DataFrame(returns_data_4, index=dates.copy())

def make_data_5():
    np.random.seed(123)
    d = dates.copy()
    data = {
        "AAPL": np.random.normal(0.0008, 0.018, len(d)),
        "GOOGL": np.random.normal(0.0006, 0.016, len(d)),
        "TSLA": np.random.normal(0.0012, 0.035, len(d)),
        "BRK-B": np.random.normal(0.0004, 0.012, len(d)),
        "JPM": np.random.normal(0.0005, 0.020, len(d)),
    }
    return pd.DataFrame(data, index=d)

def make_factor():
    np.random.seed(42)
    return pd.DataFrame({
        "Mkt-RF": np.random.normal(0.0003, 0.012, n),
        "SMB": np.random.normal(0.0001, 0.008, n),
        "HML": np.random.normal(0.0002, 0.009, n),
    }, index=dates.copy())

def make_ar1_data():
    np.random.seed(456)
    d = dates.copy()
    n2 = len(d)
    def gen_ar1(n, phi, mu, sigma):
        eps = np.random.normal(0, sigma, n)
        r = np.zeros(n)
        r[0] = mu + eps[0]
        for t in range(1, n):
            r[t] = mu + phi * (r[t-1] - mu) + eps[t]
        return r

    ret_data = {
        "Stock_A": gen_ar1(n2, phi=0.1, mu=0.0005, sigma=0.015),
        "Stock_B": gen_ar1(n2, phi=-0.05, mu=0.0003, sigma=0.018),
        "Stock_C": gen_ar1(n2, phi=0.0, mu=0.0008, sigma=0.022),
    }
    ret_df = pd.DataFrame(ret_data, index=d)
    price_data = {
        "Stock_A": 100 * np.cumprod(1 + ret_df["Stock_A"]),
        "Stock_B": 100 * np.cumprod(1 + ret_df["Stock_B"]),
        "Stock_C": 100 * np.cumprod(1 + ret_df["Stock_C"]),
    }
    price_df = pd.DataFrame(price_data, index=d)
    return ret_df, price_df

def make_ff_factor():
    np.random.seed(789)
    d = dates.copy()
    return pd.DataFrame({
        "Mkt-RF": np.random.normal(0.0003, 0.012, len(d)),
        "SMB": np.random.normal(0.0001, 0.008, len(d)),
        "HML": np.random.normal(0.0002, 0.009, len(d)),
    }, index=d)

# ============================================================
# 导入考生代码
# ============================================================
from quant_test_part1_basics import (
    count_missing, check_index_quality, compute_max_drawdown,
    annualized_stats, compute_beta, compute_alpha_beta,
    find_most_correlated, rolling_correlation,
)
from quant_test_part2_intermediate import (
    historical_var, historical_cvar, equal_weight_portfolio,
    sharpe_ratio, minimum_variance_portfolio,
    cumulative_return_curve, calmar_ratio,
)
from quant_test_part3_advanced import (
    compute_autocorrelation, max_rolling_volatility_date,
    bollinger_breakout_ratio, moving_average_crossover_backtest,
    fama_french_regression,
)

# ============================================================
# 评分系统
# ============================================================
class Scorer:
    def __init__(self):
        self.total = 0
        self.results = OrderedDict()
        self.details = []

    def test(self, name, points, func, expected, rtol=1e-3, atol=1e-6, **kwargs):
        try:
            result = func(**kwargs)
        except Exception as e:
            self.details.append(f"  X {name}: exception {type(e).__name__}: {str(e)[:100]}")
            self.results[name] = 0
            return

        try:
            passed = self._compare(result, expected, rtol, atol)
        except Exception as e:
            self.details.append(f"  X {name}: compare error {type(e).__name__}: {str(e)[:100]}")
            self.results[name] = 0
            return

        if passed:
            self.total += points
            self.results[name] = points
            self.details.append(f"  OK {name}: +{points}")
        else:
            self.results[name] = 0
            self.details.append(f"  X {name}: +0 (mismatch)")

    def test_price(self, name, points, func, expected_price, **kwargs):
        try:
            result = func(**kwargs)
        except Exception as e:
            self.details.append(f"  X {name}: exception {type(e).__name__}: {str(e)[:100]}")
            self.results[name] = 0
            return

        try:
            if isinstance(result, pd.Series) and isinstance(expected_price, pd.Series):
                result, expected_price = result.align(expected_price, join="inner")
                passed = np.allclose(result.values, expected_price.values, rtol=1e-2, atol=1e-3)
            elif isinstance(result, np.ndarray):
                passed = np.allclose(result, expected_price, rtol=1e-2, atol=1e-2)
            else:
                passed = self._compare_scalar(result, expected_price, rtol=1e-2, atol=1e-3)
        except Exception as e:
            self.details.append(f"  X {name}: compare error: {str(e)[:100]}")
            self.results[name] = 0
            return

        if passed:
            self.total += points
            self.results[name] = points
            self.details.append(f"  OK {name}: +{points}")
        else:
            self.results[name] = 0
            self.details.append(f"  X {name}: +0 (mismatch)")

    def _compare(self, result, expected, rtol, atol):
        if isinstance(expected, pd.Series):
            if not isinstance(result, pd.Series):
                return False
            expected = expected.reindex(result.index) if len(expected) != len(result) else expected
            return np.allclose(result.values, expected.values, rtol=rtol, atol=atol, equal_nan=True)
        elif isinstance(expected, pd.DataFrame):
            if not isinstance(result, pd.DataFrame):
                return False
            return np.allclose(result.values, expected.values, rtol=rtol, atol=atol, equal_nan=True)
        elif isinstance(expected, tuple):
            if not isinstance(result, tuple) or len(result) != len(expected):
                return False
            return all(self._compare(r, e, rtol, atol) for r, e in zip(result, expected))
        elif isinstance(expected, dict):
            if not isinstance(result, dict):
                return False
            if set(expected.keys()) != set(result.keys()):
                return False
            return all(self._compare(result[k], expected[k], rtol, atol) for k in expected)
        elif isinstance(expected, np.ndarray):
            return np.allclose(result, expected, rtol=rtol, atol=atol)
        else:
            return self._compare_scalar(result, expected, rtol, atol)

    def _compare_scalar(self, result, expected, rtol, atol):
        return np.isclose(result, expected, rtol=rtol, atol=atol)

    def print_report(self):
        print("\n" + "=" * 60)
        print("  Quantitative Programming Test - Score Report")
        print("=" * 60)
        for detail in self.details:
            print(detail)
        print("-" * 60)
        score = self.total
        max_score = 100
        print(f"  Total: {score}/{max_score} ({score/max_score*100:.1f}%)")
        print("-" * 60)

        if score >= 85:
            level = "Quantitative Researcher Level"
            desc = "Your coding skills are fully sufficient for writing a quantitative thesis."
        elif score >= 65:
            level = "Quantitative Analyst Level"
            desc = "Solid foundation. You can start a quant thesis but need to strengthen some advanced skills."
        elif score >= 40:
            level = "Beginner Quant"
            desc = "You have basics but need systematic study of financial econometrics and time series analysis."
        else:
            level = "Foundation Stage"
            desc = "Build up Python data analysis fundamentals first, then move into quantitative finance."
        print(f"  Rating: {level}")
        print(f"  {desc}")
        print("=" * 60)
        return score


# ============================================================
# 参考答案
# ============================================================
from quant_test_solutions import (
    solution_1_1, solution_1_2, solution_1_3,
    solution_2_1, solution_2_2, solution_2_3,
    solution_3_1, solution_3_2,
    solution_4_1, solution_4_2,
    solution_5_1, solution_5_2, solution_5_3,
    solution_6_1, solution_6_2,
    solution_7_1, solution_7_2, solution_7_3,
    solution_8_1,
    solution_9_1,
)

# ============================================================
# 运行所有测试
# ============================================================
def run_all_tests():
    s = Scorer()

    df4 = make_data_4()
    df5 = make_data_5()
    factor = make_factor()
    ar1_ret, ar1_price = make_ar1_data()

    # ---------- Part 1 ----------
    print("\n[Part 1] Basic Data Processing...")

    s.test("1.1 count_missing", 2, count_missing,
           solution_1_1(df4), df=df4.copy())

    s.test("1.2 check_index_quality", 2, check_index_quality,
           solution_1_2(df4), df=df4.copy())

    s.test("1.3 compute_max_drawdown", 4, compute_max_drawdown,
           solution_1_3(df4), returns_df=df4.copy())

    s.test("2.1 annualized_stats", 4, annualized_stats,
           solution_2_1(df4), returns_df=df4.copy())

    s.test("2.2 compute_beta", 4, compute_beta,
           solution_2_2(df4, factor["Mkt-RF"]),
           returns_df=df4.copy(), market_returns=factor["Mkt-RF"].copy())

    s.test("2.3 compute_alpha_beta", 4, compute_alpha_beta,
           solution_2_3(df4, factor["Mkt-RF"]),
           returns_df=df4.copy(), market_returns=factor["Mkt-RF"].copy())

    s.test("3.1 find_most_correlated", 4, find_most_correlated,
           solution_3_1(df4, "AAPL"), returns_df=df4.copy(), target="AAPL")

    s.test_price("3.2 rolling_correlation", 6, rolling_correlation,
                 solution_3_2(df4, "AAPL", "GOOGL", 60),
                 returns_df=df4.copy(), stock1="AAPL", stock2="GOOGL", window=60)

    # ---------- Part 2 ----------
    print("[Part 2] Risk Metrics & Portfolio...")

    s.test("4.1 historical_var", 4, historical_var,
           solution_4_1(df5, 0.95), returns_df=df5.copy(), confidence=0.95)

    s.test("4.2 historical_cvar", 6, historical_cvar,
           solution_4_2(df5, 0.95), returns_df=df5.copy(), confidence=0.95)

    s.test("5.1 equal_weight_portfolio", 6, equal_weight_portfolio,
           solution_5_1(df5), returns_df=df5.copy())

    eq_ret = solution_5_1(df5)
    s.test("5.2 sharpe_ratio", 6, sharpe_ratio,
           solution_5_2(eq_ret, 0.03),
           portfolio_returns=eq_ret.copy(), risk_free_rate=0.03)

    s.test("5.3 minimum_variance_portfolio", 6, minimum_variance_portfolio,
           solution_5_3(df5), returns_df=df5.copy())

    s.test_price("6.1 cumulative_return_curve", 6, cumulative_return_curve,
                 solution_6_1(eq_ret), returns_series=eq_ret.copy())

    s.test("6.2 calmar_ratio", 6, calmar_ratio,
           solution_6_2(eq_ret), returns_series=eq_ret.copy())

    # ---------- Part 3 ----------
    print("[Part 3] Time Series & Advanced Modeling...")

    s.test("7.1 compute_autocorrelation", 4, compute_autocorrelation,
           solution_7_1(ar1_ret, 1), returns_df=ar1_ret.copy(), lag=1)

    s.test("7.2 max_rolling_volatility_date", 4, max_rolling_volatility_date,
           solution_7_2(ar1_ret, 20), returns_df=ar1_ret.copy(), window=20)

    s.test("7.3 bollinger_breakout_ratio", 4, bollinger_breakout_ratio,
           solution_7_3(ar1_price, 20, 2),
           price_df=ar1_price.copy(), window=20, num_std=2)

    # 8.1 (10分) — returns a dict, compare manually
    stock_a_price = ar1_price["Stock_A"].copy()
    try:
        result = moving_average_crossover_backtest(
            stock_a_price, short_window=20, long_window=50
        )
        expected = solution_8_1(stock_a_price, 20, 50)
        pts = 10
        sub_ok = 0
        sub_tests = 0
        for key in ["total_return", "sharpe_ratio", "max_drawdown", "win_rate"]:
            if key in result and key in expected:
                sub_tests += 1
                if s._compare(result[key], expected[key], rtol=0.1, atol=0.1):
                    sub_ok += 1
        if "cumulative_return" in result and "cumulative_return" in expected:
            sub_tests += 1
            cum_r = result["cumulative_return"]
            cum_e = expected["cumulative_return"]
            if isinstance(cum_r, pd.Series) and isinstance(cum_e, pd.Series):
                cum_r, cum_e = cum_r.align(cum_e, join="inner")
                if np.allclose(cum_r.values, cum_e.values, rtol=0.05, atol=0.05):
                    sub_ok += 1

        if sub_ok == sub_tests and sub_tests > 0:
            s.total += pts
            s.results["8.1 moving_average_crossover_backtest"] = pts
            s.details.append(f"  OK 8.1 moving_average_crossover_backtest: +{pts}")
        else:
            s.results["8.1 moving_average_crossover_backtest"] = 0
            s.details.append(f"  X 8.1 moving_average_crossover_backtest: +0 ({sub_ok}/{sub_tests} passed)")
    except Exception as e:
        s.results["8.1 moving_average_crossover_backtest"] = 0
        s.details.append(f"  X 8.1 moving_average_crossover_backtest: +0 (error: {str(e)[:80]})")

    # 9.1 (8分)
    ff = make_ff_factor()
    stock_a_ret = ar1_ret["Stock_A"].copy()
    s.test("9.1 fama_french_regression", 8, fama_french_regression,
           solution_9_1(stock_a_ret, ff),
           stock_returns=stock_a_ret, factor_df=ff.copy())

    s.print_report()
    return s.total

if __name__ == "__main__":
    run_all_tests()
