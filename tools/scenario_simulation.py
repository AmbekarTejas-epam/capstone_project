import pandas as pd
from typing import Optional, Dict


class ScenarioSimulationTool:
    def __init__(self, sales_path: str):
        self.sales_df = pd.read_csv(sales_path, parse_dates=["date"])

    # -------------------------------
    # 1. Promo Impact Simulation
    # -------------------------------
    def simulate_promo(
        self,
        sku_id: str,
        store_id: Optional[str] = None,
        discount_pct: float = 20.0,
        expected_lift_pct: float = 30.0
    ) -> Dict:

        df = self.sales_df[self.sales_df["sku_id"] == sku_id]

        if store_id:
            df = df[df["store_id"] == store_id]

        baseline_units = df["units_sold"].mean()

        simulated_units = baseline_units * (1 + expected_lift_pct / 100)
        simulated_price = df["price"].mean() * (1 - discount_pct / 100)
        simulated_revenue = simulated_units * simulated_price

        return {
            "scenario": "promo_simulation",
            "baseline_avg_units": round(baseline_units, 2),
            "simulated_units": round(simulated_units, 2),
            "simulated_price": round(simulated_price, 2),
            "simulated_revenue": round(simulated_revenue, 2),
            "assumptions": {
                "discount_pct": discount_pct,
                "expected_lift_pct": expected_lift_pct
            }
        }

    # -------------------------------
    # 2. Price Change Simulation
    # -------------------------------
    def simulate_price_change(
        self,
        sku_id: str,
        price_change_pct: float = 10.0,
        demand_elasticity: float = -1.2
    ) -> Dict:

        df = self.sales_df[self.sales_df["sku_id"] == sku_id]

        baseline_price = df["price"].mean()
        baseline_units = df["units_sold"].mean()

        demand_change_pct = demand_elasticity * (price_change_pct / 100)
        simulated_units = baseline_units * (1 + demand_change_pct)
        simulated_price = baseline_price * (1 + price_change_pct / 100)
        simulated_revenue = simulated_units * simulated_price

        return {
            "scenario": "price_change_simulation",
            "baseline_price": round(baseline_price, 2),
            "baseline_units": round(baseline_units, 2),
            "simulated_price": round(simulated_price, 2),
            "simulated_units": round(simulated_units, 2),
            "simulated_revenue": round(simulated_revenue, 2),
            "assumptions": {
                "price_change_pct": price_change_pct,
                "demand_elasticity": demand_elasticity
            }
        }

    # -------------------------------
    # 3. Supply Shortage Simulation
    # -------------------------------
    def simulate_supply_shortage(
        self,
        sku_id: str,
        supply_drop_pct: float = 30.0
    ) -> Dict:

        df = self.sales_df[self.sales_df["sku_id"] == sku_id]

        baseline_units = df["units_sold"].mean()

        max_sellable_units = baseline_units * (1 - supply_drop_pct / 100)
        lost_sales_units = baseline_units - max_sellable_units

        return {
            "scenario": "supply_shortage_simulation",
            "baseline_units": round(baseline_units, 2),
            "max_sellable_units": round(max_sellable_units, 2),
            "lost_sales_units": round(lost_sales_units, 2),
            "assumptions": {
                "supply_drop_pct": supply_drop_pct
            }
        }
