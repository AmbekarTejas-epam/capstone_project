import pandas as pd
from typing import Optional, Dict

print("✅ trend_analysis tool LOADED")

class TrendAnalysisTool:
    def __init__(self, sales_path: str):
        self.sales_df = pd.read_csv(sales_path, parse_dates=["date"])
        
    def analyze(
        self,
        sku_id: Optional[str] = None,
        store_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        time_granularity: str = "monthly"
    ) -> Dict:
        print("🚨 trend_analysis tool CALLED")

        df = self.sales_df.copy()

        # --- Filters ---
        if sku_id:
            df = df[df["sku_id"] == sku_id]

        if store_id:
            df = df[df["store_id"] == store_id]

        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]

        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]

        # --- Time aggregation ---
        if time_granularity == "monthly":
            df["period"] = df["date"].dt.to_period("M").astype(str)
        elif time_granularity == "weekly":
            df["period"] = df["date"].dt.to_period("W").astype(str)
        else:
            raise ValueError("Invalid time_granularity")

        grouped = (
            df.groupby("period")
            .agg(
                units_sold=("units_sold", "sum"),
                revenue=("revenue", "sum")
            )
            .reset_index()
        )

        # --- Trend computation ---
        if len(grouped) < 2:
            trend = "flat"
            growth_rate = 0.0
        else:
            first = grouped.iloc[0]["revenue"]
            last = grouped.iloc[-1]["revenue"]
            growth_rate = ((last - first) / first) * 100 if first != 0 else 0.0

            if growth_rate > 5:
                trend = "increasing"
            elif growth_rate < -5:
                trend = "decreasing"
            else:
                trend = "flat"

        peak_period = grouped.loc[grouped["revenue"].idxmax()]["period"]
        lowest_period = grouped.loc[grouped["revenue"].idxmin()]["period"]
        
        data_coverage = {
        "start_date": df["date"].min().strftime("%Y-%m-%d"),
        "end_date": df["date"].max().strftime("%Y-%m-%d"),
        "num_records": len(df),
        "num_periods": len(grouped)
    }

        return {
            "time_series": grouped,
            "overall_trend": trend,
            "growth_rate_pct": round(growth_rate, 2),
            "peak_period": peak_period,
            "lowest_period": lowest_period,
            "data_coverage": data_coverage
        }
