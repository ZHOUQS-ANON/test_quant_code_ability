# Agent Guide

本仓库是一个 pandas / NumPy 量化编程能力测试项目。后续 agent 在这里工作时，应优先保持题目、测试和参考答案之间的边界清晰，只在用户明确要求的范围内修改代码。

## Project Structure

- `other_practice/quant_test_part1_basics.py`: Part 1，基础数据处理、统计分析、相关性分析题目。包含待完成的 TODO 函数。
- `other_practice/quant_test_part2_intermediate.py`: Part 2，VaR/CVaR、组合构建、绩效归因题目。包含待完成的 TODO 函数。
- `other_practice/quant_test_part3_advanced.py`: Part 3，时间序列特征、移动均线回测、Fama-French 回归题目。包含待完成的 TODO 函数。
- `other_practice/test_runner.py`: 自动评分器。通过导入三份题目文件中的函数，并与参考答案对比计算 100 分制成绩。
- `other_practice/quant_test_solutions.py`: 参考答案。用于评分比对，除非用户明确要求维护参考答案，否则不要修改。

## Working Rules

- 不要修改各题文件顶部的“数据准备（请勿修改）”部分。
- 解题时只替换对应 TODO 函数中的 `pass`，避免改动函数名、参数名和返回类型。
- 不要通过修改 `test_runner.py` 或 `quant_test_solutions.py` 来让测试通过。
- 保持实现简洁，优先使用 pandas / NumPy 的向量化 API。
- 返回值要匹配测试器预期的类型：
  - 缺失值、Beta、VaR、CVaR、自相关等列级结果返回 `pd.Series`。
  - 年化统计、alpha/beta、最大滚动波动率等表格结果返回 `pd.DataFrame`。
  - 最小方差组合权重返回 `numpy.ndarray`，顺序必须与 `returns_df.columns` 一致。
  - 移动平均回测返回包含指定 key 的 `dict`。
- 注意金融指标约定：
  - 年化交易日数为 252。
  - 最大回撤、VaR、CVaR 以正数表示损失幅度。
  - 累计净值通常使用 `(1 + returns).cumprod()`。
  - 回测信号需要 `shift(1)`，体现 1 天交易延迟。

## Testing

从 `other_practice` 目录运行评分器：

```bash
cd other_practice
python test_runner.py
```

评分器会输出每一题的通过情况和总分。若在仓库根目录运行，导入路径可能不正确，因此优先从 `other_practice` 目录执行。

## Safety Rules

禁止批量删除文件或目录。不要使用以下命令或等价操作：

- `del /s`
- `rd /s`
- `rmdir /s`
- `Remove-Item -Recurse`
- `rm -rf`

如果确实需要删除文件，只能一次删除一个明确路径的文件。需要批量清理时，停止操作并请用户手动删除。

## Before Finishing

- 确认没有改动参考答案或评分逻辑，除非用户明确要求。
- 运行 `python test_runner.py` 并记录分数或失败项；如果无法运行，说明原因。
- 保持改动集中，避免格式化无关文件或引入额外依赖。
