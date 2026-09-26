"""
Logistics Predictive Modeling and Optimization Engine
Week 4: Predictive Modeling & Optimization
Author: Saurabh Kumar

This module builds, evaluates, and deploys a predictive pipeline for delivery duration
forecasting in supply chain networks, along with an operational optimization framework.

Key Capabilities:
1. Feature Preprocessing (One-Hot Encoding + Standardization via Pipeline)
2. Multi-Model Benchmark (Linear Regression, Decision Tree, Random Forest, Gradient Boosting)
3. Full Validation (Train/Test Split + 5-Fold Cross-Validation)
4. Evaluation Metrics (MAE, RMSE, R²)
5. Feature Importance Extraction & Diagnostic Visualizations
6. Operational Optimization (Risk-Aware Dispatching & Capacity Allocation)
7. Model Serialization (.joblib export)
"""

import os
import argparse
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


CATEGORICAL_COLS = ["region", "shipping_mode", "vehicle_type", "weather"]
NUMERIC_COLS = ["distance_km", "shipment_volume", "fuel_price"]
TARGET_COL = "delivery_time_days"


def build_preprocessor() -> ColumnTransformer:
    """Builds a scikit-learn ColumnTransformer for categorical and numerical features."""
    return ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_COLS),
            ("num", StandardScaler(), NUMERIC_COLS),
        ]
    )


def build_pipeline(model=None) -> Pipeline:
    """Constructs an end-to-end Pipeline with preprocessing and regressor."""
    if model is None:
        model = RandomForestRegressor(
            n_estimators=220,
            max_depth=14,
            min_samples_leaf=3,
            random_state=42,
        )
    return Pipeline(
        steps=[
            ("preprocess", build_preprocessor()),
            ("model", model),
        ]
    )


class LogisticsForecastingEngine:
    """End-to-end delivery time predictive model and decision-support engine."""

    def __init__(self, data_path: str = "data/processed/logistics_cleaned.csv"):
        self.data_path = data_path
        self.df = None
        self.pipeline = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.test_predictions = None
        self.metrics = {}

    def load_and_split(self, test_size: float = 0.2, random_state: int = 42):
        """Loads data and creates reproducible train/test splits."""
        if not os.path.exists(self.data_path):
            alt_path = os.path.join("..", "..", self.data_path)
            if os.path.exists(alt_path):
                self.data_path = alt_path
            else:
                raise FileNotFoundError(f"Dataset not found at {self.data_path}")

        self.df = pd.read_csv(self.data_path)
        X = self.df[CATEGORICAL_COLS + NUMERIC_COLS]
        y = self.df[TARGET_COL]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        print(f"Loaded {len(self.df)} records. Training set: {len(self.X_train)}, Test set: {len(self.X_test)}")

    def benchmark_models(self) -> pd.DataFrame:
        """Evaluates multiple candidate models on the training set using 5-Fold Cross-Validation."""
        candidates = {
            "Linear Regression": LinearRegression(),
            "Decision Tree": DecisionTreeRegressor(max_depth=8, random_state=42),
            "Random Forest": RandomForestRegressor(n_estimators=220, max_depth=14, min_samples_leaf=3, random_state=42),
            "Gradient Boosting": GradientBoostingRegressor(n_estimators=150, max_depth=4, learning_rate=0.08, random_state=42),
        }

        results = []
        cv = KFold(n_splits=5, shuffle=True, random_state=42)

        for name, model in candidates.items():
            pipe = build_pipeline(model)
            cv_scores = cross_val_score(pipe, self.X_train, self.y_train, cv=cv, scoring="neg_mean_squared_error")
            cv_rmse = np.sqrt(-cv_scores).mean()
            cv_r2 = cross_val_score(pipe, self.X_train, self.y_train, cv=cv, scoring="r2").mean()
            results.append({"Model": name, "CV RMSE (days)": round(cv_rmse, 4), "CV R2": round(cv_r2, 4)})

        benchmark_df = pd.DataFrame(results)
        print("\n" + "=" * 50)
        print("MODEL BENCHMARK RESULTS (5-Fold CV)")
        print("=" * 50)
        print(benchmark_df.to_string(index=False))
        print("=" * 50)
        return benchmark_df

    def train_champion_model(self):
        """Trains the primary production Random Forest regressor pipeline."""
        self.pipeline = build_pipeline()
        self.pipeline.fit(self.X_train, self.y_train)
        self.test_predictions = self.pipeline.predict(self.X_test)

        mae = mean_absolute_error(self.y_test, self.test_predictions)
        rmse = np.sqrt(mean_squared_error(self.y_test, self.test_predictions))
        r2 = r2_score(self.y_test, self.test_predictions)

        # 5-Fold CV on entire feature space
        X_all = self.df[CATEGORICAL_COLS + NUMERIC_COLS]
        y_all = self.df[TARGET_COL]
        cv = KFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = cross_val_score(self.pipeline, X_all, y_all, cv=cv, scoring="neg_mean_squared_error")
        cv_rmse = np.sqrt(-cv_scores).mean()

        self.metrics = {
            "MAE": round(mae, 3),
            "RMSE": round(rmse, 3),
            "R2": round(r2, 3),
            "CV_RMSE": round(cv_rmse, 3),
        }

        print("\n" + "=" * 50)
        print("CHAMPION MODEL TEST EVALUATION")
        print("=" * 50)
        print(f"Mean Absolute Error (MAE):    {self.metrics['MAE']:.3f} days")
        print(f"Root Mean Squared Error (RMSE): {self.metrics['RMSE']:.3f} days")
        print(f"R-squared Score (R2):         {self.metrics['R2']:.3f}")
        print(f"5-Fold Cross-Validation RMSE: {self.metrics['CV_RMSE']:.3f} days")
        print("=" * 50)

    def generate_diagnostic_plots(self, output_dir: str = "outputs/figures"):
        """Generates and saves feature importance and actual vs predicted residual plots."""
        os.makedirs(output_dir, exist_ok=True)
        if self.pipeline is None:
            raise ValueError("Train model first before generating diagnostic plots.")

        # Extract feature names after One-Hot Encoding
        preprocessor = self.pipeline.named_steps["preprocess"]
        cat_encoder = preprocessor.named_transformers_["cat"]
        encoded_cats = list(cat_encoder.get_feature_names_out(CATEGORICAL_COLS))
        all_features = encoded_cats + NUMERIC_COLS

        rf_model = self.pipeline.named_steps["model"]
        importances = rf_model.feature_importances_

        # Plot 1: Feature Importance
        feat_df = pd.DataFrame({"Feature": all_features, "Importance": importances})
        feat_df = feat_df.sort_values(by="Importance", ascending=True)

        plt.figure(figsize=(10, 6))
        plt.barh(feat_df["Feature"], feat_df["Importance"], color="#1f77b4", edgecolor="black", alpha=0.85)
        plt.title("Random Forest Feature Importance — Delivery Time Prediction", fontsize=13, fontweight="bold")
        plt.xlabel("Gini Importance Score", fontsize=11)
        plt.grid(axis="x", linestyle="--", alpha=0.5)
        plt.tight_layout()
        feat_path = os.path.join(output_dir, "feature_importance.png")
        plt.savefig(feat_path, dpi=300)
        plt.close()
        print(f"Saved feature importance plot to {feat_path}")

        # Plot 2: Actual vs Predicted Scatter with 45-degree reference line
        plt.figure(figsize=(8, 6))
        plt.scatter(self.y_test, self.test_predictions, alpha=0.6, color="#2ca02c", edgecolors="black", s=40)
        min_val = min(self.y_test.min(), self.test_predictions.min())
        max_val = max(self.y_test.max(), self.test_predictions.max())
        plt.plot([min_val, max_val], [min_val, max_val], "r--", linewidth=2, label="Perfect Forecast (y = x)")
        plt.title(f"Predicted vs Actual Delivery Time (R² = {self.metrics.get('R2', 0.789):.3f})", fontsize=13, fontweight="bold")
        plt.xlabel("Actual Delivery Time (Days)", fontsize=11)
        plt.ylabel("Predicted Delivery Time (Days)", fontsize=11)
        plt.legend(frameon=True)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        resid_path = os.path.join(output_dir, "model_actual_vs_predicted.png")
        plt.savefig(resid_path, dpi=300)
        plt.close()
        print(f"Saved actual vs predicted diagnostic plot to {resid_path}")

    def save_model(self, model_path: str = "outputs/models/rf_delivery_model.joblib"):
        """Serializes the trained pipeline for production scoring."""
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(self.pipeline, model_path)
        print(f"Exported serialized model pipeline to {model_path}")

    def run_optimization_simulation(self, sample_size: int = 20) -> pd.DataFrame:
        """
        Demonstrates the conceptual operational optimization layer:
        Calculates predicted delivery times, flags SLA breach risks,
        and recommends dynamic vehicle assignment to minimize delay risks.
        """
        sample = self.df.sample(sample_size, random_state=42).copy()
        features = sample[CATEGORICAL_COLS + NUMERIC_COLS]
        sample["predicted_delivery_days"] = self.pipeline.predict(features)
        sample["sla_buffer_days"] = sample["scheduled_days"] - sample["predicted_delivery_days"]
        
        # Risk classification
        sample["risk_tier"] = np.where(
            sample["sla_buffer_days"] < 0,
            "Critical SLA Breach",
            np.where(sample["sla_buffer_days"] < 0.5, "At-Risk Window", "Safe / On-Schedule"),
        )

        # Operational optimization recommendation rule
        def recommend_action(row):
            if row["risk_tier"] == "Critical SLA Breach":
                if row["shipping_mode"] != "Same Day":
                    return "Escalate Mode: Upgrade to Express Air / Priority Transit"
                return "Reassign Depot: Dispatch from Nearest Regional Hub"
            elif row["risk_tier"] == "At-Risk Window":
                return "Optimize Route: Assign Dedicated Direct Van"
            return "Standard Dispatch: Consolidate Route"

        sample["recommended_action"] = sample.apply(recommend_action, axis=1)
        
        print("\n" + "=" * 70)
        print("SAMPLE OPTIMIZATION DISPATCH RECOMMENDATIONS")
        print("=" * 70)
        display_cols = ["order_id", "region", "shipping_mode", "scheduled_days", "predicted_delivery_days", "risk_tier", "recommended_action"]
        print(sample[display_cols].head(8).to_string(index=False))
        print("=" * 70)
        return sample


def main():
    parser = argparse.ArgumentParser(description="Train and evaluate logistics delivery time forecasting pipeline.")
    parser.add_argument("--data", type=str, default="data/processed/logistics_cleaned.csv", help="Input processed CSV path.")
    parser.add_argument("--model-out", type=str, default="outputs/models/rf_delivery_model.joblib", help="Output path for joblib model.")
    parser.add_argument("--fig-out", type=str, default="outputs/figures", help="Directory for output evaluation figures.")
    args = parser.parse_args()

    engine = LogisticsForecastingEngine(data_path=args.data)
    engine.load_and_split()
    engine.benchmark_models()
    engine.train_champion_model()
    engine.generate_diagnostic_plots(output_dir=args.fig_out)
    engine.save_model(model_path=args.model_out)
    engine.run_optimization_simulation(sample_size=15)


if __name__ == "__main__":
    main()
