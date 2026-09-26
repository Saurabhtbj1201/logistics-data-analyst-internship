# Week 1: Strategic Planning and Data Exploration in Logistics

## Executive Overview
This module initiates the **Logistics Data Analyst Internship** by establishing the business problem context, formalizing operational Key Performance Indicators (KPIs), surveying relevant literature, and outlining a 7-stage analytical data-science roadmap.

---

## 1. Operational Scenario & Business Context
The project models an enterprise multi-depot regional distribution network serving diverse customer orders across 5 operating territories (`West`, `East`, `Central`, `North`, `South`):
- **Warehousing:** 5 fulfillment depots (`WH-Central`, `WH-North`, `WH-East`, `WH-West`, `WH-South`).
- **Fleet Dynamics:** Heterogeneous transport resources (Light Vans, Medium Trucks, Heavy Long-Haul Fleet).
- **Service Levels:** 4 customer delivery tiers (Same Day, First Class, Second Class, Standard).
- **Transit Dynamics:** Route distances (8 to 450 km), cargo payload volumes, regional fuel price fluctuations, and dynamic weather states (`Clear`, `Rain`, `Fog`, `Storm`).
- **Strategic Goal:** Resolve persistent delivery delays (initial late rate of 44.00%), control logistics expenditure ($1,242.32 average per shipment), and maximize order profit contribution.

---

## 2. Key Performance Indicators (KPIs)

| KPI | Mathematical Formulation | Operational Business Objective |
| :--- | :--- | :--- |
| **On-Time Delivery Rate (OTD)** | $\frac{\text{On-Time Shipments}}{\text{Total Shipments}} \times 100$ | Measure contract service reliability and customer SLA compliance. |
| **Late Delivery Rate** | $\frac{\text{Late Shipments}}{\text{Total Shipments}} \times 100$ | Identify operational bottlenecks, fulfillment risk, and penalty exposure. |
| **Average Delivery Time** | $\frac{1}{N}\sum \text{actual\_delivery\_days}$ | Monitor baseline transit velocity and lead times across shipping tiers. |
| **Transport Cost per Shipment** | $\frac{1}{N}\sum \text{transport\_cost}$ | Audit haulage spend and identify vehicle/route inefficiencies. |
| **Average Profit per Order** | $\frac{1}{N}\sum (\text{order\_value} - \text{logistics\_cost})$ | Link operational logistics performance directly to net commercial profitability. |

---

## 3. Data Science Methodologies

| Methodology | Application in Logistics Pipeline |
| :--- | :--- |
| **Descriptive Statistics** | Establish baseline KPI benchmarks, variance, and regional fulfillment distribution. |
| **Correlation Analysis** | Quantify linear associations between transit duration, route distance, cost, and load size. |
| **Supervised Regression** | Forecast continuous delivery duration (`delivery_time_days`) prior to vehicle dispatch. |
| **Unsupervised Clustering** | Partition shipments via K-Means into operational profiles for differentiated fleet allocation. |
| **Constrained Optimization** | Formulate integer linear programming models to minimize transport cost subject to vehicle capacity and SLA limits. |

---

## 4. End-to-End Strategic Roadmap
```
1. Data Ingestion & Source Validation
   └── Ingest raw transaction logs, weather, and depot dispatches
2. Data Cleaning & Preprocessing (Week 2)
   └── Median/Mode imputation, IQR outlier screening, StandardScaler
3. Advanced EDA & Visualization (Week 3)
   └── SLA comparisons, regional heatmaps, correlation matrix, K-Means clustering
4. Feature Engineering & Preprocessing Pipelines (Week 4)
   └── ColumnTransformer, one-hot encoding, SLA risk buffers
5. Predictive Modeling & Cross-Validation (Week 4)
   └── Linear Regression, Decision Trees, Random Forest, Gradient Boosting
6. Constrained Optimization & Scenario Analysis (Week 4)
   └── Risk-aware dispatching, dynamic vehicle assignment, capacity balancing
7. Deployment, Monitoring & Governance
   └── Daily feature drift tracking, automated retraining triggers, KPI dashboards
```

---

## 5. Directory Structure
```
week-01-strategic-planning/
├── README.md
├── report/
│   └── Week_1_Strategic_Planning_and_Data_Exploration.docx
└── notebooks/
    └── week_01_strategy.ipynb
```

---

## 6. How to Run
To run the interactive exploratory strategy notebook:
```bash
jupyter notebook notebooks/week_01_strategy.ipynb
```
Or execute all cells in VS Code / Jupyter Lab to review the baseline KPI calculations and regional aggregations.
