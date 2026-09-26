# Logistics Data Analyst Internship: End-to-End Analytics, Modeling & Optimization

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.2%2B-orange.svg)](https://scikit-learn.org/)
[![Progress](https://img.shields.io/badge/Internship_Progress-4%2F4_Tasks_Complete-success.svg)](https://github.com/Saurabhtbj1201/logistics-data-analyst-internship)

**Author:** Saurabh Kumar  
**GitHub Repository:** [https://github.com/Saurabhtbj1201/logistics-data-analyst-internship](https://github.com/Saurabhtbj1201/logistics-data-analyst-internship)  
**Internship Duration:** 4 Weeks (24-Aug-2026 to 21-Sep-2026)  
**Status:** Completed (4/4 Weekly Milestones Delivered)

---

## Executive Summary

Modern logistics and supply chain systems operate under razor-thin margins and stringent Service Level Agreements (SLAs). Inefficiencies in route scheduling, fleet allocation, and transit forecasting directly lead to delivery delays, escalating fuel expenses, and customer churn.

This repository encapsulates the full 4-week **Logistics Data Analyst Internship** project. It presents a complete, enterprise-grade data science lifecycle that transforms raw logistics transaction records into measurable business intelligence, automated preprocessing pipelines, predictive delivery duration forecasts, and operational dispatch optimization policies.

---

## Repository Architecture

```text
logistics-data-analyst-internship/
│
├── README.md                                          # Master project documentation
├── requirements.txt                                  # Pinned Python package dependencies
├── .gitignore                                        # Git version control exclusions
│
├── data/
│   ├── raw/
│   │   ├── README.md                                 # Raw data dictionary and reference context
│   │   ├── logistics_orders.csv                      # Raw dataset with simulated data-quality anomalies
│   │   └── simulated_logistics_dataset.csv           # Ground-truth benchmark simulation dataset (1,500 records)
│   │
│   └── processed/
│       └── logistics_cleaned.csv                     # Fully audited, imputed, and scaled dataset
│
├── week-01-strategic-planning/
│   ├── README.md                                     # Week 1 briefing: Strategy, KPIs, and roadmap
│   ├── report/
│   │   └── Week_1_Strategic_Planning_and_Data_Exploration.docx
│   └── notebooks/
│       └── week_01_strategy.ipynb                    # Interactive strategy and exploratory notebook
│
├── week-02-data-preprocessing/
│   ├── README.md                                     # Week 2 briefing: Cleaning, IQR screening, scaling
│   ├── report/
│   │   └── Week_2_Data_Collection_Cleaning_and_Preprocessing.docx
│   ├── notebooks/
│   │   └── week_02_preprocessing.ipynb               # Interactive data quality & transformation notebook
│   └── src/
│       └── preprocessing.py                          # Reusable preprocessing pipeline script
│
├── week-03-eda-visualization/
│   ├── README.md                                     # Week 3 briefing: EDA, KPIs, correlation, clustering
│   ├── report/
│   │   └── Week_3_Advanced_Data_Analysis_and_Visualization.docx
│   ├── notebooks/
│   │   └── week_03_eda.ipynb                         # Exploratory data analysis notebook
│   └── visualizations/
│       ├── delivery_by_mode.png                      # Delivery duration across SLA shipping tiers
│       ├── late_by_region.png                        # Late delivery rate across operating territories
│       ├── distance_delivery.png                     # Route distance vs. delivery transit time
│       └── cost_distribution.png                     # Transportation cost frequency distribution
│
├── week-04-predictive-modeling/
│   ├── README.md                                     # Week 4 briefing: ML models, validation, optimization
│   ├── report/
│   │   └── Week_4_Predictive_Modeling_and_Optimization.docx
│   ├── notebooks/
│   │   └── week_04_prediction.ipynb                  # Machine learning training & optimization notebook
│   └── src/
│       └── model.py                                  # Predictive pipeline & decision-support engine
│
└── outputs/
    ├── figures/
    │   ├── delivery_by_mode.png
    │   ├── late_by_region.png
    │   ├── distance_delivery.png
    │   ├── cost_distribution.png
    │   ├── feature_importance.png                    # Gini feature importances for transit duration
    │   └── model_actual_vs_predicted.png             # Out-of-sample prediction diagnostics
    └── models/
        └── rf_delivery_model.joblib                  # Serialized production Random Forest pipeline
```

---

## 4-Week Milestone Breakdown

### Week 1 — Strategic Planning and Data Exploration in Logistics
- **Business Scenario:** Formulated a multi-depot regional fulfillment network serving orders across 5 territories (`West`, `East`, `Central`, `North`, `South`) through 5 warehouses and a heterogeneous fleet.
- **KPI Framework:** Established 5 vital supply chain performance indicators:
  1. *On-Time Delivery (OTD) Rate*
  2. *Late Delivery Rate*
  3. *Average Delivery Time*
  4. *Transport Cost per Shipment*
  5. *Average Profit per Order*
- **Research & References:** Grounded in industry-standard datasets including the *DataCo Smart Supply Chain for Big Data Analysis* and the *UCI Online Retail* benchmark.
- **Deliverables:** Complete strategic report docx, technical README, and executed exploratory notebook `week_01_strategy.ipynb`.

### Week 2 — Data Collection, Cleaning & Preprocessing
- **Data Quality Audit:** Ingested 1,500 raw shipment records containing 10 missing distances, 10 missing cargo volumes, 10 unrecorded weather labels, and 30 artificial transport cost outliers.
- **Domain-Justified Imputations:** Implemented median imputation for skewed numerical variables (`distance_km` and `shipment_volume`) and mode imputation for categorical attributes (`weather`).
- **Statistical Outlier Detection:** Applied Tukey's Interquartile Range (IQR) rule on `transport_cost` with fences $[Q_1 - 1.5 \times \text{IQR}, Q_3 + 1.5 \times \text{IQR}]$, successfully flagging and auditing 30 outlier records.
- **Feature Normalization:** Standardized numerical predictors using `StandardScaler` to remove scale dominance.
- **Deliverables:** Reusable pipeline script `src/preprocessing.py`, interactive audit notebook `week_02_preprocessing.ipynb`, and cleaned dataset `data/processed/logistics_cleaned.csv`.

### Week 3 — Advanced Data Analysis & Visualization
- **KPI Baseline Measurement:** Audited the benchmark operational performance:
  - On-Time Delivery Rate: **56.00%**
  - Late Delivery Rate: **44.00%**
  - Average Delivery Time: **3.56 days**
  - Average Transport Cost: **$1,242.32**
  - Average Order Value: **$2,332.97**
  - Average Profit: **$977.08**
- **Diagnostic Visualizations:** Generated publication-quality figures:
  - *Delivery Time by Shipping Mode:* Evaluated transit velocity across SLA tiers.
  - *Late Delivery Rate by Region:* Pinpointed severe delay bottlenecks in Northern and Central territories (>45% late).
  - *Distance vs. Delivery Time:* Analyzed transit duration dispersion ($r = 0.462$).
  - *Transport Cost Distribution:* Uncovered cost skewness and tail risk.
- **Unsupervised Segmentation:** Implemented K-Means clustering ($k=3$) to create differentiated fleet routing profiles:
  - *Cluster 0 (Short Distance / Low Cost):* Local van parcel delivery.
  - *Cluster 1 (Mid Distance / High Volume):* Medium-duty bulk pallet transport.
  - *Cluster 2 (Long Haul / High Cost):* Long-distance freight relay candidate.
- **Deliverables:** Complete analytical report docx, high-resolution PNG visualizations, and notebook `week_03_eda.ipynb`.

### Week 4 — Predictive Modeling & Optimization
- **Problem Formulation:** Cast delivery duration prediction as a supervised regression task using operational features available pre-dispatch (`region`, `shipping_mode`, `vehicle_type`, `weather`, `distance_km`, `shipment_volume`, `fuel_price`).
- **Model Benchmark (5-Fold Cross-Validation):** Evaluated Linear Regression, Decision Trees, Random Forest, and Gradient Boosting.
- **Champion Model Performance:** Trained a tuned **Random Forest Regressor** (`n_estimators=220`, `max_depth=14`, `min_samples_leaf=3`):
  - **MAE:** **0.425 days** (~10.2 hours)
  - **RMSE:** **0.529 days** (~12.7 hours)
  - **$R^2$ Score:** **0.789** (78.9% variance explained)
  - **5-Fold CV RMSE:** **0.503 days**
- **Operational Optimization Framework:**
  - Designed an early-warning **SLA Buffer Metric** ($\text{SLA Buffer} = \text{Promised SLA} - \widehat{\text{Delivery Time}}$).
  - Formulated a constrained integer linear programming (ILP) vehicle dispatch optimization model.
  - Simulated dynamic dispatch rules that reassign critical at-risk shipments to express priority fleets.
- **Deliverables:** Production ML engine `src/model.py`, interactive modeling notebook `week_04_prediction.ipynb`, serialized model `outputs/models/rf_delivery_model.joblib`, and diagnostic evaluation plots.

---

## Key Performance Indicators & Benchmark Summary

| Analytical Domain | Metric | Result | Benchmark Significance |
| :--- | :--- | :---: | :--- |
| **Operations** | On-Time Delivery Rate | **56.00%** | Baseline reliability deficit identified for intervention. |
| **Operations** | Late Delivery Rate | **44.00%** | Target reduction to < 15% through predictive dispatch. |
| **Operations** | Average Delivery Time | **3.56 days** | Mean fulfillment lead time across all service tiers. |
| **Financial** | Average Transport Cost | **$1,242.32** | Primary operational expenditure driver. |
| **Financial** | Average Order Profit | **$977.08** | Net contribution margin per order. |
| **Machine Learning** | Test MAE | **0.425 days** | Accurate out-of-sample delivery time forecast (~10 hrs). |
| **Machine Learning** | Test RMSE | **0.529 days** | Low forecast error variance on test set. |
| **Machine Learning** | Test $R^2$ | **0.789** | Explains nearly 80% of real-world transit variation. |
| **Machine Learning** | 5-Fold CV RMSE | **0.503 days** | Verified model stability across all data partitions. |

---

## Installation & Setup

### Prerequisites
- Python 3.9, 3.10, 3.11, or 3.12
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Saurabhtbj1201/logistics-data-analyst-internship.git
cd logistics-data-analyst-internship
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## How to Execute Pipelines

### Run Data Preprocessing (Week 2):
```bash
python week-02-data-preprocessing/src/preprocessing.py --input data/raw/logistics_orders.csv --output data/processed/logistics_cleaned.csv
```

### Run Model Training, Evaluation & Optimization (Week 4):
```bash
python week-04-predictive-modeling/src/model.py --data data/processed/logistics_cleaned.csv --model-out outputs/models/rf_delivery_model.joblib --fig-out outputs/figures
```

### Run Interactive Jupyter Notebooks:
```bash
jupyter notebook
```
Navigate to any of the weekly notebooks to step through the interactive analyses:
- `week-01-strategic-planning/notebooks/week_01_strategy.ipynb`
- `week-02-data-preprocessing/notebooks/week_02_preprocessing.ipynb`
- `week-03-eda-visualization/notebooks/week_03_eda.ipynb`
- `week-04-predictive-modeling/notebooks/week_04_prediction.ipynb`

---

## Production Deployment & Governance Roadmap

1. **Inference Microservice:** Wrap `rf_delivery_model.joblib` in a lightweight FastAPI endpoint to generate real-time transit predictions at order checkout.
2. **Dynamic SLA Recalibration:** Feed forecasted delivery times back to the customer-facing storefront to present dynamic, achievable delivery dates instead of static promises.
3. **Automated Dispatch Rules:** Integrate SLA risk buffers into warehouse management systems (WMS) to automate express carrier selection when delay probability exceeds 30%.
4. **Model Drift Monitoring:** Implement automated weekly drift checks (KS-tests on distances, PSI on categorical shifts, and tracking rolling MAE) to trigger automated pipeline retraining.

---

## License & Attribution

This project is developed as part of the **Logistics Data Analyst Internship** by Saurabh Kumar.  
Distributed under the MIT License. See `LICENSE` for further details.
