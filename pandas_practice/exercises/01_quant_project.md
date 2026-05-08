# 练习 01：用 pandas 完成一个迷你量化项目

本练习围绕 `data/daily_bars.csv` 展开。数据字段如下：

| 字段 | 含义 |
| --- | --- |
| `date` | 交易日期 |
| `symbol` | 股票代码，`BENCH` 是基准指数 |
| `sector` | 行业 |
| `open` / `high` / `low` / `close` | OHLC 价格 |
| `adj_close` | 复权收盘价 |
| `volume` | 成交量 |

## 任务 1：加载并清洗数据

在 `load_price_data` 中完成：

- 读取 CSV，并把 `date` 解析为 datetime。
- 去掉 `symbol` 前后的空格。
- 将价格和成交量字段转为数值。
- 如果 `close` 缺失，用 `adj_close` 填补。
- 删除重复的 `date + symbol` 记录。
- 按 `symbol`、`date` 排序。

你应该得到一个整洁的长表 DataFrame。

## 任务 2：构建价格宽表

在 `make_wide_prices` 中完成：

- 行索引用 `date`。
- 列索引用 `symbol`。
- 值使用 `adj_close`。
- 日期从小到大排序。

提示：可以使用 `pivot` 或 `pivot_table`。

## 任务 3：计算收益率

在 `calculate_returns` 中完成：

- 使用 `pct_change` 计算日收益率。
- 保留和价格矩阵相同的索引、列。
- 第一行可以保留为 `NaN`。

## 任务 4：生成技术特征

在 `add_technical_features` 中按 `symbol` 分组计算：

- `daily_return`：复权收盘价日收益率。
- `ma_5`：5 日均线。
- `ma_20`：20 日均线。
- `volatility_20`：20 日收益率滚动标准差。
- `dollar_volume`：`close * volume`。

注意：rolling 计算必须在每个 symbol 内部完成，不能把不同股票连在一起算。

## 任务 5：动量信号

在 `build_monthly_momentum_signal` 中完成：

- 用 `lookback` 个交易日前后的价格变化计算动量。
- 每月末取一次信号。
- 排除 `BENCH`。
- 每个月只保留动量最高的 `top_n` 只股票，等权。

函数返回一个月度权重表：行是再平衡月份，列是股票代码，值是权重。

## 任务 6：策略回测与绩效评估

在 `backtest_long_only_momentum` 中完成：

- 将月度权重扩展到日频。
- 权重要 `shift(1)`，避免使用当天收盘后才知道的信号交易当天。
- 计算组合日收益率。

在 `summarize_performance` 中完成：

- `total_return`
- `annual_return`
- `annual_volatility`
- `sharpe`
- `max_drawdown`
- `win_rate`

## 延伸挑战

- 对比策略与 `BENCH` 的累计净值曲线。
- 增加交易成本，例如每次调仓按换手率扣除 0.1%。
- 改成行业中性：每个行业选 1 只动量最强的股票。
- 尝试 20、60、120 日不同 lookback，并汇总绩效。
