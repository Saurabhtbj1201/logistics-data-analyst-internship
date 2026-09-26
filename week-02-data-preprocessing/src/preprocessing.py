"""
Logistics Data Preprocessing Module
Week 2: Data Collection, Cleaning & Preprocessing
Author: Saurabh Kumar

This script implements a reproducible data preprocessing pipeline for logistics shipment data:
1. Data Ingestion & Quality Assessment
2. Missing Value Imputation (Median for numeric, Mode for categorical)
3. Outlier Screening using Interquartile Range (IQR) on operational transport costs
4. Feature Normalization & Scaling using StandardScaler
5. Export of Cleaned and Transformed Datasets
"""

import os
import argparse
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


class LogisticsDataPreprocessor:
    """
    Robust data preprocessing pipeline for logistics and supply chain records.
    """

    def __init__(self, raw_filepath: str):
        self.raw_filepath = raw_filepath
        self.df = None
        self.df_cleaned = None
        self.scaler = StandardScaler()
        self.cleaning_stats = {}

    def load_data(self) -> pd.DataFrame:
        """Loads raw dataset from disk."""
        if not os.path.exists(self.raw_filepath):
            raise FileNotFoundError(f"Input file not found: {self.raw_filepath}")
        
        self.df = pd.read_csv(self.raw_filepath)
        self.cleaning_stats["initial_rows"] = len(self.df)
        self.cleaning_stats["initial_cols"] = len(self.df.columns)
        self.cleaning_stats["initial_missing"] = self.df.isnull().sum().to_dict()
        print(f"Loaded {len(self.df)} records from {self.raw_filepath}")
        return self.df

    def handle_missing_values(self) -> pd.DataFrame:
        """
        Imputes missing values using domain-justified techniques:
        - Median imputation for skewed numeric features (distance_km, shipment_volume)
        - Mode imputation for operational categorical features (weather)
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        df = self.df.copy()

        # Numeric median imputation
        if "distance_km" in df.columns:
            dist_median = df["distance_km"].median()
            dist_missing = df["distance_km"].isnull().sum()
            df["distance_km"] = df["distance_km"].fillna(dist_median)
            self.cleaning_stats["imputed_distance_missing"] = int(dist_missing)
            self.cleaning_stats["distance_median"] = float(dist_median)

        if "shipment_volume" in df.columns:
            vol_median = df["shipment_volume"].median()
            vol_missing = df["shipment_volume"].isnull().sum()
            df["shipment_volume"] = df["shipment_volume"].fillna(vol_median)
            self.cleaning_stats["imputed_volume_missing"] = int(vol_missing)
            self.cleaning_stats["volume_median"] = float(vol_median)

        # Categorical mode imputation
        if "weather" in df.columns:
            weather_mode = df["weather"].mode()[0]
            weather_missing = df["weather"].isnull().sum()
            df["weather"] = df["weather"].fillna(weather_mode)
            self.cleaning_stats["imputed_weather_missing"] = int(weather_missing)
            self.cleaning_stats["weather_mode"] = str(weather_mode)

        self.df = df
        return self.df

    def screen_outliers(self, factor: float = 1.5, remove: bool = True) -> pd.DataFrame:
        """
        Flags and screens outliers in transport_cost using the IQR rule:
        [Q1 - 1.5 * IQR, Q3 + 1.5 * IQR]
        """
        if "transport_cost" not in self.df.columns:
            return self.df

        q1 = self.df["transport_cost"].quantile(0.25)
        q3 = self.df["transport_cost"].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - factor * iqr
        upper_bound = q3 + factor * iqr

        is_outlier = ~self.df["transport_cost"].between(lower_bound, upper_bound)
        outlier_count = int(is_outlier.sum())

        self.cleaning_stats["cost_q1"] = float(q1)
        self.cleaning_stats["cost_q3"] = float(q3)
        self.cleaning_stats["cost_iqr"] = float(iqr)
        self.cleaning_stats["cost_lower_bound"] = float(lower_bound)
        self.cleaning_stats["cost_upper_bound"] = float(upper_bound)
        self.cleaning_stats["outliers_screened"] = outlier_count

        if remove:
            self.df = self.df[~is_outlier].copy()
            self.cleaning_stats["rows_after_outlier_removal"] = len(self.df)
        else:
            self.df["cost_is_outlier"] = is_outlier.astype(int)

        return self.df

    def scale_features(self) -> pd.DataFrame:
        """
        Standardizes continuous numerical features (distance_km, shipment_volume)
        using StandardScaler (zero mean, unit variance).
        """
        features_to_scale = [col for col in ["distance_km", "shipment_volume"] if col in self.df.columns]
        if features_to_scale:
            scaled_array = self.scaler.fit_transform(self.df[features_to_scale])
            self.df["distance_scaled"] = scaled_array[:, 0]
            self.df["volume_scaled"] = scaled_array[:, 1]
            self.cleaning_stats["scaled_features"] = features_to_scale

        self.df_cleaned = self.df.copy()
        return self.df_cleaned

    def run_pipeline(self, remove_outliers: bool = False) -> pd.DataFrame:
        """
        Executes the entire end-to-end preprocessing pipeline.
        Note: For preserving the complete 1,500 record baseline in downstream modeling,
        outliers are flagged or retained unless remove_outliers=True is specified.
        """
        self.load_data()
        self.handle_missing_values()
        self.screen_outliers(factor=1.5, remove=remove_outliers)
        self.scale_features()
        return self.df_cleaned

    def print_summary(self):
        """Displays data quality assessment and transformation results."""
        print("=" * 60)
        print("LOGISTICS DATA PREPROCESSING PIPELINE SUMMARY")
        print("=" * 60)
        print(f"Initial Records Loaded:       {self.cleaning_stats.get('initial_rows', 0)}")
        print(f"Missing Distances Imputed:    {self.cleaning_stats.get('imputed_distance_missing', 0)} (Median: {self.cleaning_stats.get('distance_median', 0):.2f})")
        print(f"Missing Volumes Imputed:      {self.cleaning_stats.get('imputed_volume_missing', 0)} (Median: {self.cleaning_stats.get('volume_median', 0):.2f})")
        print(f"Missing Weather Imputed:      {self.cleaning_stats.get('imputed_weather_missing', 0)} (Mode: {self.cleaning_stats.get('weather_mode', '')})")
        print(f"Outlier Screening Bounds:     [{self.cleaning_stats.get('cost_lower_bound', 0):.2f}, {self.cleaning_stats.get('cost_upper_bound', 0):.2f}]")
        print(f"Outlier Records Detected:     {self.cleaning_stats.get('outliers_screened', 0)}")
        print(f"Final Cleaned Records:        {len(self.df_cleaned) if self.df_cleaned is not None else 0}")
        print("=" * 60)

    def export_data(self, output_filepath: str):
        """Exports the processed DataFrame to CSV."""
        if self.df_cleaned is None:
            raise ValueError("No cleaned data available to export. Run run_pipeline() first.")
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        self.df_cleaned.to_csv(output_filepath, index=False)
        print(f"Exported cleaned dataset to {output_filepath}")


def main():
    parser = argparse.ArgumentParser(description="Clean and preprocess logistics order dataset.")
    parser.add_argument("--input", type=str, default="data/raw/logistics_orders.csv", help="Path to input raw CSV.")
    parser.add_argument("--output", type=str, default="data/processed/logistics_cleaned.csv", help="Path to output cleaned CSV.")
    parser.add_argument("--remove-outliers", action="store_true", help="Remove IQR cost outliers instead of just flagging them.")
    args = parser.parse_args()

    # Fallback to local files if executed from week-02 directory
    input_path = args.input
    output_path = args.output
    if not os.path.exists(input_path):
        alt_path = os.path.join("..", "..", input_path)
        if os.path.exists(alt_path):
            input_path = alt_path
            output_path = os.path.join("..", "..", output_path)

    preprocessor = LogisticsDataPreprocessor(input_path)
    preprocessor.run_pipeline(remove_outliers=args.remove_outliers)
    preprocessor.print_summary()
    preprocessor.export_data(output_path)


if __name__ == "__main__":
    main()
