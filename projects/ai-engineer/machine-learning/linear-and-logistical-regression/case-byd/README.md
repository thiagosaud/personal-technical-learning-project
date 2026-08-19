# 🏗️ BYD Machine Learning Case

[![Python](https://img.shields.io/badge/python-%3E%3D3.12-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![scikit--learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![pandas](https://img.shields.io/badge/pandas-data%20analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../../../LICENSE)

Educational machine learning project applied to BYD vehicle technical specifications.

The pipeline runs:

1. Simple linear regression.
2. Multiple linear regression.
3. Logistic regression.

At the end, three PNG charts are generated with data, predictions, fitted
curves, and model metrics.

## ⚠️ Scope

This project is a technical and educational demonstration.

The data is defined directly in [layer/data/etl.py](layer/data/etl.py).
There is currently no ingestion from a CSV file, API, or database.

The metrics are calculated using the same data used for training. Therefore,
they do not represent a generalized evaluation on unseen data.

## 🧱 Architecture

```text
main.py
   │
   ├── ETLLayer
   │      └── DataFrame sorted by weight
   │
   ├── ModelTrainerLayer
   │      ├── Simple linear regression
   │      ├── Multiple linear regression
   │      └── Logistic regression
   │
   └── ModelVisualizerLayer
          └── Three PNG charts
```

## 📁 Structure

```text
case-byd/
├── config/
│   └── schema/data/vehicle.py       # Column contract
├── layer/
│   ├── data/etl.py                  # Data construction and sorting
│   ├── machine_learning/
│   │   └── model_trainer.py         # Training and metrics
│   └── visualizer/
│       └── model_visualizer.py      # Charts
├── src/case_byd/
│   └── __init__.py
├── main.py                          # Entry point
├── pyproject.toml                   # Dependencies and CLI
└── uv.lock                          # Locked dependencies
```

## 📋 Variables

| Column                       | Description                               |
| ---------------------------- | ----------------------------------------- |
| `MODEL`                      | Vehicle model name                        |
| `WEIGHT_KG`                  | Weight in kilograms                       |
| `POWER_CV`                   | Power in horsepower                       |
| `ACCELERATION_FROM_0_TO_100` | 0 to 100 km/h acceleration time           |
| `BATTERY_KWH`                | Battery capacity                          |
| `CONSUMPTION_MJ_KM`          | Consumption in MJ/km                      |
| `IS_PURE_ELECTRIC`           | Binary classification of electric vehicle |

## 🧪 Experiments

| Case | Model                      | Inputs                  | Output                       | Metric   |
| ---- | -------------------------- | ----------------------- | ---------------------------- | -------- |
| 1    | Simple linear regression   | `WEIGHT_KG`             | `CONSUMPTION_MJ_KM`          | R²       |
| 2    | Multiple linear regression | `WEIGHT_KG`, `POWER_CV` | `ACCELERATION_FROM_0_TO_100` | R²       |
| 3    | Logistic regression        | `BATTERY_KWH`           | `IS_PURE_ELECTRIC`           | Accuracy |

Training is implemented in
[layer/machine_learning/model_trainer.py](layer/machine_learning/model_trainer.py).

## ⚙️ Requirements

- Python `3.12` or later
- uv
- pandas
- NumPy
- scikit-learn
- Matplotlib
- adjustText

## 🚀 Installation

Run from this directory:

```bash
uv sync --frozen
```

To install the BYD project's dependencies from the monorepo root:

```bash
cd projects/ai-engineer/machine-learning/linear-and-logistical-regression/case-byd
uv sync --frozen
```

## ▶️ Usage

```bash
uv run python main.py
```

You can also use the CLI command declared by the project:

```bash
uv run case-byd
```

The command prints the R² and accuracy values and saves the charts in the
current working directory.

## 🖼️ Outputs

| File                            | Content                                      |
| ------------------------------- | -------------------------------------------- |
| `byd_case1_linear_simples.png`  | Weight versus energy consumption             |
| `byd_case2_linear_multiple.png` | Actual values versus predicted acceleration  |
| `byd_case3_logistic.png`        | Estimated probability of an electric vehicle |

The PNG files are locally generated artifacts.

## 🔍 Quality

From the monorepo root:

```bash
pnpm run lint:code:py
pnpm run lint:security:py
pnpm run lint:security:semgrep
pnpm run test:py
```

## 📄 License

This project follows the MIT license defined in the
[root repository](../../../../../../LICENSE).

---

A small laboratory for applied data, models, and visualization 🤖
