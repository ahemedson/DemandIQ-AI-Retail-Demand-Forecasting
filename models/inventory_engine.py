import math
import pandas as pd


class InventoryEngine:
    """
    Calculates inventory planning metrics using
    forecasted demand and current inventory.
    """

    def __init__(
        self,
        forecast_df: pd.DataFrame,
        current_stock: int,
        lead_time: int = 7,
        service_level: float = 0.95
    ):

        self.forecast_df = forecast_df.copy()

        self.current_stock = current_stock

        self.lead_time = lead_time

        self.service_level = service_level

    # --------------------------------------------------
    # Average Daily Demand
    # --------------------------------------------------

    def average_daily_demand(self):

        return self.forecast_df["Forecast"].mean()

    # --------------------------------------------------
    # Lead Time Demand
    # --------------------------------------------------

    def lead_time_demand(self):

        return (
            self.average_daily_demand()
            * self.lead_time
        )

    # --------------------------------------------------
    # Demand Standard Deviation
    # --------------------------------------------------

    def demand_std(self):

        return self.forecast_df["Forecast"].std()

    # --------------------------------------------------
    # Safety Stock
    # --------------------------------------------------

    def safety_stock(self):

        z_score = 1.65 if self.service_level >= 0.95 else 1.28

        return (
            z_score
            * self.demand_std()
            * math.sqrt(self.lead_time)
        )

    # --------------------------------------------------
    # Reorder Point
    # --------------------------------------------------

    def reorder_point(self):

        return (
            self.lead_time_demand()
            + self.safety_stock()
        )

    # --------------------------------------------------
    # Days of Inventory
    # --------------------------------------------------

    def inventory_days(self):

        avg = self.average_daily_demand()

        if avg == 0:
            return 0

        return self.current_stock / avg

    # --------------------------------------------------
    # Stockout Risk
    # --------------------------------------------------

    def stockout_risk(self):

        if self.current_stock < self.reorder_point():
            return "High"

        if self.current_stock < (
            self.reorder_point() * 1.25
        ):
            return "Medium"

        return "Low"

    # --------------------------------------------------
    # Purchase Recommendation
    # --------------------------------------------------

    def purchase_quantity(self):

        recommendation = (
            self.reorder_point()
            - self.current_stock
        )

        return max(
            0,
            round(recommendation)
        )

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(self):

        return {

            "Current Stock": self.current_stock,

            "Average Daily Demand":
                round(
                    self.average_daily_demand(),
                    2
                ),

            "Lead Time Demand":
                round(
                    self.lead_time_demand(),
                    2
                ),

            "Safety Stock":
                round(
                    self.safety_stock(),
                    2
                ),

            "Reorder Point":
                round(
                    self.reorder_point(),
                    2
                ),

            "Days of Inventory":
                round(
                    self.inventory_days(),
                    1
                ),

            "Stockout Risk":
                self.stockout_risk(),

            "Recommended Purchase":
                self.purchase_quantity()

        }