# pandas / NumPy Quant Practice

这是一个 pandas / NumPy 量化编程能力测试项目，用来练习金融数据处理、风险指标、投资组合构建、时间序列特征和因子回归。

## 项目结构

- `other_practice/quant_test_part1_basics.py`: 基础数据清洗、统计分析、Beta/Alpha、相关性分析练习。
- `other_practice/quant_test_part2_intermediate.py`: VaR/CVaR、等权组合、Sharpe、最小方差组合、累计收益和 Calmar Ratio 练习。
- `other_practice/quant_test_part3_advanced.py`: 自相关、滚动波动率、布林带、均线交叉回测、Fama-French 三因子回归练习。
- `other_practice/test_runner.py`: 自动评分器，按 100 分制对练习函数进行评分。
- `other_practice/quant_test_solutions.py`: 参考答案，供评分器比对使用。
- `agent.md`: 给后续 agent 的项目说明和操作规则。

## 运行评分器

```bash
cd other_practice
python test_runner.py
```

当前题目文件中的 TODO 函数尚未实现，评分器会显示对应失败项。解题时建议只替换 TODO 函数里的 `pass`，不要修改数据准备区、评分器或参考答案。
