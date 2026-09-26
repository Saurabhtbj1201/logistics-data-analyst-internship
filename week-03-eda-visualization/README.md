# Week 3: Advanced Data Analysis & Visualization in Logistics

## Executive Overview
This module conducts deep Exploratory Data Analysis (EDA) on the 1,500 logistics records. It calculates baseline operational KPIs, produces 4 targeted business visualizations, computes multivariable correlation metrics, and performs K-Means clustering to create operational shipment segments.

---

## 1. Key Performance Indicator (KPI) Analysis

| KPI | Simulated Result | Benchmark Evaluation |
| :--- | :--- | :--- |
| **On-Time Delivery Rate** | **56.00%** | Critical performance deficit; 44% of orders violate promised delivery window. |
| **Late Delivery Rate** | **44.00%** | Requires operational root-cause analysis across regions and shipping tiers. |
| **Average Delivery Time** | **3.56 days** | Average transit elapsed time across all service categories. |
| **Average Transport Cost** | **$1,242.32** | Key cost driver impacting net margin per delivery route. |
| **Average Order Value** | **$2,332.97** | Average gross merchandise value per customer consignment. |
| **Average Profit per Order** | **$977.08** | Net contribution margin after modeled transportation expenses. |

---

## 2. Core Visualizations & Operational Interpretations

### Visualization 1: Average Delivery Time by Shipping Mode
- **File:** `visualizations/delivery_by_mode.png`
- **Insight:** Highlights transit velocity across SLA tiers: Same Day (~1.2 days), First Class (~2.1 days), Second Class (~3.1 days), and Standard (~4.8 days). Confirms that priority tiers meet absolute time targets, but standard shipments experience the highest schedule variability.

### Visualization 2: Late Delivery Rate by Region
- **File:** `visualizations/late_by_region.png`
- **Insight:** Compares delay percentages across the 5 operating territories (West, East, Central, North, South). Uncovers that northern and central corridors suffer late rates exceeding 45%, highlighting regional road congestion, distance dispersion, or warehouse dispatch bottlenecks.

### Visualization 3: Route Distance vs. Delivery Time
- **File:** `visualizations/distance_delivery.png`
- **Insight:** Demonstrates a positive correlation ($r = 0.462$) between transit distance and elapsed transit days. However, the substantial vertical scatter indicates that distance alone does not determine delivery time—weather events, vehicle selection, and warehouse dispatch delays introduce large variance.

### Visualization 4: Transportation Cost Distribution
- **File:** `visualizations/cost_distribution.png`
- **Insight:** Illustrates the unimodal, slightly right-skewed distribution of haulage expenses, centered around $1,242.32 with a long tail extending beyond $2,500 for long-haul expedited dispatches.

---

## 3. Correlation Analysis

| Operational Variable | Correlation with `delivery_time_days` ($r$) | Direction & Practical Meaning |
| :--- | :--- | :--- |
| `distance_km` | **+0.462** | Moderate positive: longer transit routes generally require more delivery days. |
| `transport_cost` | **+0.495** | Moderate positive: shipments taking longer incur higher fuel and driver costs. |
| `order_value` | **+0.234** | Weak positive: higher-value shipments often involve bulkier items or specialized handling. |
| `shipment_volume` | **+0.165** | Mild positive: larger loads require longer loading/unloading cycles. |
| `profit` | **+0.030** | Near zero: profitability is largely decoupled from transit duration alone. |

---

## 4. Unsupervised K-Means Shipment Segmentation

| Cluster | Avg Distance (km) | Avg Volume (units) | Avg Cost ($) | Avg Delivery (days) | Operational Fleet Strategy |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **0** | 103.4 km | 24.7 | $1,011.90 | 3.22 days | **Local Parcel Delivery:** Small vans, high-frequency consolidated neighborhood routes. |
| **1** | 127.8 km | 62.9 | $1,477.00 | 3.72 days | **Regional Bulk Transport:** Medium-duty trucks optimized for high payload density. |
| **2** | 256.4 km | 30.4 | $1,655.20 | 4.34 days | **Long-Haul Inter-City Transit:** Dedicated highway freight; candidate for relay hubs and rail. |

---

## 5. Directory Structure
```
week-03-eda-visualization/
├── README.md
├── report/
│   └── Week_3_Advanced_Data_Analysis_and_Visualization.docx
├── notebooks/
│   └── week_03_eda.ipynb
└── visualizations/
    ├── delivery_by_mode.png
    ├── late_by_region.png
    ├── distance_delivery.png
    └── cost_distribution.png
```

---

## 6. How to Run
```bash
jupyter notebook week-03-eda-visualization/notebooks/week_03_eda.ipynb
```
Running the notebook reproduces all statistical summaries, correlation tables, and high-resolution visual plots.
