from models.inventory_engine import InventoryEngine
from utils.logger import Logger


logger = Logger.get_logger()


class InventoryService:
    """
    Service layer for inventory intelligence.
    """

    def __init__(
        self,
        forecast_df,
        current_stock,
        lead_time=7,
        service_level=0.95
    ):

        self.engine = InventoryEngine(
            forecast_df=forecast_df,
            current_stock=current_stock,
            lead_time=lead_time,
            service_level=service_level
        )

    # --------------------------------------------------
    # Inventory Summary
    # --------------------------------------------------

    def get_summary(self):

        logger.info(
            "Generating inventory summary."
        )

        return self.engine.summary()

    # --------------------------------------------------
    # Average Daily Demand
    # --------------------------------------------------

    def average_daily_demand(self):

        return self.engine.average_daily_demand()

    # --------------------------------------------------
    # Safety Stock
    # --------------------------------------------------

    def safety_stock(self):

        return self.engine.safety_stock()

    # --------------------------------------------------
    # Reorder Point
    # --------------------------------------------------

    def reorder_point(self):

        return self.engine.reorder_point()

    # --------------------------------------------------
    # Inventory Days
    # --------------------------------------------------

    def inventory_days(self):

        return self.engine.inventory_days()

    # --------------------------------------------------
    # Stockout Risk
    # --------------------------------------------------

    def stockout_risk(self):

        return self.engine.stockout_risk()

    # --------------------------------------------------
    # Purchase Recommendation
    # --------------------------------------------------

    def purchase_quantity(self):

        return self.engine.purchase_quantity()