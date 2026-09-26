# Week 2: Data Collection, Cleaning & Preprocessing

## Executive Overview
This module implements a production-ready, reproducible data cleaning and preprocessing pipeline for raw supply chain records. It audits data quality, handles missing values using domain-sound imputations, screens statistical outliers using Tukey's IQR fences, and scales continuous features for machine learning algorithms.

---

## 1. Data Quality Assessment

| Variable | Data Type | Missing Count | Data Quality Issue | Imputation / Treatment Method |
| :--- | :--- | :--- | :--- | :--- |
| `distance_km` | Numeric (Float) | 10 records | Right-skewed distribution; mean is sensitive to extreme route lengths. | **Median Imputation** (Preserves route distribution median ~126 km). |
| `shipment_volume` | Numeric (Float) | 10 records | Heavy-tailed load proxy; skewed by large batch bulk orders. | **Median Imputation** (Preserves median cargo payload ~29.8 units). |
| `weather` | Categorical | 10 records | Missing transit meteorological observation. | **Mode Imputation** (Replaces nulls with dominant state `'Clear'`). |
| `transport_cost` | Numeric (Float) | 0 records | Artificial extreme cost values distorting averages and standard errors. | **IQR Statistical Screening** ($[Q_1 - 1.5\\times\\text{IQR}, Q_3 + 1.5\\times\\text{IQR}]$). |
| `distance_km` & `shipment_volume` | Numeric | 0 records | Differing orders of magnitude (hundreds of km vs tens of units). | **StandardScaler Normalization** ($\mu=0, \sigma=1$). |

---

## 2. Statistical Outlier Detection (Tukey's IQR Fences)
For operational transport cost, outlier fences were calculated as:
- **$Q_1$ (25th Percentile):** $628.59
- **$Q_3$ (75th Percentile):** $1,811.78
- **Interquartile Range (IQR):** $1,183.19
- **Lower Fence:** $628.59 - (1.5 \times 1,183.19) = -1,146.20 \rightarrow \text{Bound at } \$271.99$
- **Upper Fence:** $1,811.78 + (1.5 \times 1,183.19) = \$3,586.57$
- **Flagged Outlier Records:** 30 shipments

---

## 3. Preprocessing Demonstration Results

| Metric | Result | Description |
| :--- | :--- | :--- |
| **Records Before Cleaning** | 1,500 | Complete uncleaned operational order transactions |
| **Missing Distance Values Imputed** | 10 | Median imputed (`126.10 km`) |
| **Missing Volume Values Imputed** | 10 | Median imputed (`29.76 units`) |
| **Missing Weather Values Imputed** | 10 | Mode imputed (`Clear`) |
| **Rows Screened as Cost Outliers** | 30 | Flagged via IQR screening rule |
| **Cleaned Records Exported** | 1,500 | Available in `data/processed/logistics_cleaned.csv` |

---

## 4. Source Code & Architecture
The preprocessing logic is modularized in `src/preprocessing.py`:
- `LogisticsDataPreprocessor`: Reusable class with individual stages: `load_data()`, `handle_missing_values()`, `screen_outliers()`, and `scale_features()`.
- Command-line interface with `--input`, `--output`, and optional `--remove-outliers` flags.

```
week-02-data-preprocessing/
├── README.md
├── report/
│   └── Week_2_Data_Collection_Cleaning_and_Preprocessing.docx
├── notebooks/
│   └── week_02_preprocessing.ipynb
└── src/
    └── preprocessing.py
```

---

## 5. Execution Instructions
### Running the Preprocessing Script:
```bash
python week-02-data-preprocessing/src/preprocessing.py --input data/raw/logistics_orders.csv --output data/processed/logistics_cleaned.csv
```

### Running the Interactive Notebook:
```bash
jupyter notebook week-02-data-preprocessing/notebooks/week_02_preprocessing.ipynb
```
