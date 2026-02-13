import pandas as pd
from typing import Optional, Dict


class AnomalyDetectionTool:
    def __init__(self, sales_path: str):
        self.sales_df = pd.read_csv(sales_path, parse_dates=["date"])

    def detect(
        self,
        sku_id: Optional[str] = None,
        store_id: Optional[str] = None,
        window: int = 7,
        z_threshold: float = 2.0
    ) -> Dict:
        print("🚨 anomaly_detection tool CALLED")
        df = self.sales_df.copy()

        # --- Filters ---
        if sku_id:
            df = df[df["sku_id"] == sku_id]
        if store_id:
            df = df[df["store_id"] == store_id]

        df = df.sort_values("date")

        # --- Rolling stats ---
        df["rolling_mean"] = df["units_sold"].rolling(window).mean()
        df["rolling_std"] = df["units_sold"].rolling(window).std()

        df["z_score"] = (
            (df["units_sold"] - df["rolling_mean"]) / df["rolling_std"]
        )

        anomalies = df[
            df["z_score"].abs() > z_threshold
        ].dropna()

        # --- Severity logic ---
        anomaly_count = len(anomalies)

        if anomaly_count == 0:
            severity = "low"
        elif anomaly_count <= 2:
            severity = "medium"
        else:
            severity = "high"

        return {
            "anomalies": anomalies[
                ["date", "store_id", "sku_id", "units_sold", "z_score"]
            ],
            "anomaly_count": anomaly_count,
            "severity": severity
        }
