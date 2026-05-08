"""
参考答案 — 用于自动评分比对
"""
import numpy as np
import pandas as pd
# ============================================================
# Part 1 参考答案
# ============================================================

def solution_1_1(df):
    return df.isnull().sum()

def solution_1_2(df):
    return (df.index.is_monotonic_increasing, df.index.is_unique)

def solution_1_3(returns_df):
    prices = (1 + returns_df).cumprod() * 100
    running_max = prices.cummax()
    drawdown = (running_max - prices) / running_max
    return drawdown.max()

def solution_2_1(returns_df):
    ann_ret = returns_df.mean() * 252
    ann_vol = returns_df.std() * np.sqrt(252)
    return pd.DataFrame({"annual_return": ann_ret, "annual_vol": ann_vol})

def solution_2_2(returns_df, market):
    """计算每只股票对市场的 Beta"""
    betas = {}
    for col in returns_df.columns:
        cov = returns_df[col].cov(market)
        betas[col] = cov / market.var()
    return pd.Series(betas)

def solution_2_3(returns_df, market):
    results = {}
    for col in returns_df.columns:
        aligned = pd.concat([returns_df[col], market], axis=1).dropna()
        x = aligned.iloc[:, 1].values
        y = aligned.iloc[:, 0].values
        slope, intercept = np.polyfit(x, y, 1)
        results[col] = {"alpha": intercept * 252, "beta": slope}
    return pd.DataFrame(results).T

def solution_3_1(returns_df, target):
    corr = returns_df.corr()
    others = corr[target].drop(target)
    best = others.idxmax()
    return (best, others[best])

def solution_3_2(returns_df, s1, s2, window):
    return returns_df[s1].rolling(window).corr(returns_df[s2])

# ============================================================
# Part 2 参考答案
# ============================================================

def solution_4_1(returns_df, confidence):
    return -returns_df.quantile(1 - confidence)

def solution_4_2(returns_df, confidence):
    threshold = returns_df.quantile(1 - confidence)
    result = {}
    for col in returns_df.columns:
        tail = returns_df[col][returns_df[col] <= threshold[col]]
        result[col] = -tail.mean()
    return pd.Series(result)

def solution_5_1(returns_df):
    return returns_df.mean(axis=1)

def solution_5_2(port_returns, rf):
    excess = port_returns.mean() * 252 - rf
    vol = port_returns.std() * np.sqrt(252)
    return excess / vol

def solution_5_3(returns_df):
    cov = returns_df.cov() * 252
    n = len(returns_df.columns)
    # 没有做空约束，用解析解: w = Σ^{-1} 1 / (1^T Σ^{-1} 1)
    inv_cov = np.linalg.inv(cov.values)
    ones = np.ones(n)
    w = inv_cov @ ones / (ones @ inv_cov @ ones)
    return w

def solution_6_1(returns):
    return (1 + returns).cumprod()

def solution_6_2(returns):
    cum = (1 + returns).cumprod()
    running_max = cum.cummax()
    drawdown = (running_max - cum) / running_max
    mdd = drawdown.max()
    ann_ret = returns.mean() * 252
    return ann_ret / mdd

# ============================================================
# Part 3 参考答案
# ============================================================

def solution_7_1(returns_df, lag):
    return returns_df.apply(lambda col: col.autocorr(lag=lag))

def solution_7_2(returns_df, window):
    roll_vol = returns_df.rolling(window).std()
    results = {}
    for col in roll_vol.columns:
        max_idx = roll_vol[col].idxmax()
        results[col] = {"max_vol": roll_vol[col].max(), "date": max_idx}
    return pd.DataFrame(results).T

def solution_7_3(price_df, window, num_std):
    ma = price_df.rolling(window).mean()
    std = price_df.rolling(window).std()
    upper = ma + num_std * std
    return (price_df > upper).mean()

def solution_8_1(price, short, long_window):
    ret = price.pct_change().dropna()
    ma_short = price.rolling(short).mean()
    ma_long = price.rolling(long_window).mean()
    signal = (ma_short > ma_long).astype(int)
    signal = signal.shift(1).dropna()
    strategy_ret = signal * ret.loc[signal.index]
    cum = (1 + strategy_ret).cumprod()
    total_ret = cum.iloc[-1] - 1
    sr = strategy_ret.mean() / strategy_ret.std() * np.sqrt(252)
    mdd = (cum.cummax() - cum).div(cum.cummax()).max()
    holding_days = signal == 1
    win_days = (strategy_ret > 0) & holding_days
    win_rate = win_days.sum() / holding_days.sum() if holding_days.sum() > 0 else 0
    return {
        "cumulative_return": cum,
        "total_return": total_ret,
        "sharpe_ratio": sr,
        "max_drawdown": mdd,
        "win_rate": win_rate,
    }

def solution_9_1(stock_returns, factor_df):
    aligned = pd.concat([stock_returns, factor_df], axis=1).dropna()
    y = aligned.iloc[:, 0].values
    X = aligned.iloc[:, 1:].values
    X_with_const = np.column_stack([np.ones(len(X)), X])
    coeffs, *_ = np.linalg.lstsq(X_with_const, y, rcond=None)
    alpha_daily = coeffs[0]
    betas = coeffs[1:]
    y_pred = X_with_const @ coeffs
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r_squared = 1 - ss_res / ss_tot
    residual_std = np.std(y - y_pred)
    return {
        "alpha": alpha_daily * 252,
        "betas": betas,
        "r_squared": r_squared,
        "residual_std": residual_std,
    }
