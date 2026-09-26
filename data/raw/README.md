# Raw Data Documentation

This directory contains the raw operational data sources used across the 4-week **Logistics Data Analyst Internship** project.

## Files in this Directory

| File Name | Records | Description | Usage |
| :--- | :--- | :--- | :--- |
| `logistics_orders.csv` | 1,500 | Raw simulated logistics order records containing simulated data-quality anomalies (10 missing distances, 10 missing shipment volumes, 10 missing weather labels, and 30 IQR cost outliers). | Used in Week 2 Data Cleaning & Preprocessing pipeline to demonstrate imputation and outlier screening. |
| `simulated_logistics_dataset.csv` | 1,500 | Benchmark logistics dataset with complete ground-truth entries across all operational metrics. | Used across Week 1, Week 3 EDA, and Week 4 Predictive Modeling. |

---

## Data Dictionary

| Column Name | Data Type | Example Value | Description |
| :--- | :--- | :--- | :--- |
| `order_id` | Integer | `100001` | Unique shipment transaction identifier |
| `region` | Categorical (String) | `West`, `East`, `Central`, `North`, `South` | Operating delivery territory |
| `shipping_mode` | Categorical (String) | `Standard`, `Second Class`, `First Class`, `Same Day` | SLA service tier selected by customer |
| `vehicle_type` | Categorical (String) | `Van`, `Small Truck`, `Heavy Truck` | Fleet resource assigned to dispatch route |
| `warehouse` | Categorical (String) | `WH-Central`, `WH-North`, `WH-East`, `WH-West`, `WH-South` | Origin fulfillment warehouse |
| `weather` | Categorical (String) | `Clear`, `Rain`, `Fog`, `Storm` | Operational weather condition during transit |
| `distance_km` | Float (Numeric) | `141.28` | Calculated route transit distance in kilometers |
| `shipment_volume` | Float (Numeric) | `38.45` | Cubic volume / load proxy of the package |
| `fuel_price` | Float (Numeric) | `3.42` | Regional fuel price per liter/gallon during transit |
| `delivery_time_days` | Float (Numeric) | `3.56` | Actual elapsed transit time from dispatch to delivery |
| `scheduled_days` | Float (Numeric) | `3.00` | Promised/contracted delivery SLA duration |
| `late_delivery` | Binary (Integer) | `0` (On-Time) or `1` (Late) | Indicator whether actual delivery exceeded scheduled SLA |
| `transport_cost` | Float (Numeric) | `1242.32` | Total modeled logistical transport expense |
| `order_value` | Float (Numeric) | `2332.97` | Commercial order gross merchandise value |
| `profit` | Float (Numeric) | `977.08` | Net order contribution after operational logistics costs |

---

## Literature & Reference Context

- **DataCo Smart Supply Chain for Big Data Analysis**: Real-world supply-chain benchmark providing dispatch, shipping mode, and delayed status structures.
- **UCI Online Retail Dataset**: Public e-commerce reference used for order value and customer transaction characteristics.
- **Synthetic Simulation Purpose**: Created to ensure 100% reproducibility, zero data leakage, and realistic multi-factor logistics relationships (distance, service level, weather, load size, fleet type, and cost dynamics).
