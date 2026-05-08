# pandas 量化项目练习

这是一套面向 pandas 的小型量化练习项目。它用一份模拟日频行情数据，练习从数据清洗、收益率计算、技术指标、动量选股到简单回测和绩效评估的完整流程。

## 目录结构

```text
pandas_practice/
├── data/                         # 模拟行情数据
├── exercises/                    # 你需要填写的练习代码
├── scripts/                      # 数据生成脚本
├── solutions/                    # 参考答案
├── tests/                        # 合约测试
├── README.md
└── requirements.txt
```

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_sample_data.py
python -m solutions.reference_solution
pytest
```

默认测试会验证参考答案。完成 `exercises/quant_project.py` 后，可以这样检查自己的实现：

```bash
QUANT_MODULE=exercises.quant_project pytest
```

## 练习目标

1. 使用 `read_csv`、`to_datetime`、类型转换和去重清洗行情数据。
2. 使用 `pivot` / `unstack` 构建宽表价格矩阵。
3. 使用 `pct_change`、`groupby`、`rolling` 计算收益率、均线和波动率。
4. 使用 `resample` 做月度信号和再平衡。
5. 使用 DataFrame 权重矩阵实现向量化策略回测。
6. 计算累计收益、年化收益、年化波动、夏普比率、最大回撤和胜率。

## 建议学习顺序

先读 [exercises/01_quant_project.md](/Users/a0/Documents/pypractice/pandas_practice/exercises/01_quant_project.md)，再补全 [exercises/quant_project.py](/Users/a0/Documents/pypractice/pandas_practice/exercises/quant_project.py)。卡住时对照 [solutions/reference_solution.py](/Users/a0/Documents/pypractice/pandas_practice/solutions/reference_solution.py)。

数据是本地生成的模拟数据，不代表任何真实证券，也不构成投资建议。
