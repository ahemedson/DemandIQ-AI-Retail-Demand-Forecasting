from ai.ai_report_generator import AIReportGenerator


class InventoryInsights:
    """
    Generates inventory analysis using the selected
    analysis engine.
    """

    def __init__(
        self,
        inventory_summary
    ):

        self.summary = inventory_summary

        self.report_generator = AIReportGenerator()

    # --------------------------------------------------
    # Generate Report
    # --------------------------------------------------

    def generate(
        self,
        engine,
        analysis_type
    ):

        return self.report_generator.generate(

            engine=engine,

            module="inventory",

            analysis_type=analysis_type,

            variables=self._prompt_variables(),

            fallback_data={

                "summary": self.summary

            }

        )

    # --------------------------------------------------
    # Prompt Variables
    # --------------------------------------------------

    def _prompt_variables(self):

        summary = self.summary

        return {

            # Current Inventory
            "current_stock":
                round(
                    summary["Current Stock"],
                    2
                ),

            "average_daily_demand":
                round(
                    summary["Average Daily Demand"],
                    2
                ),

            "days_of_inventory":
                round(
                    summary["Days of Inventory"],
                    2
                ),

            # Inventory Planning
            "safety_stock":
                round(
                    summary["Safety Stock"],
                    2
                ),

            "reorder_point":
                round(
                    summary["Reorder Point"],
                    2
                ),

            "recommended_purchase":
                round(
                    summary["Recommended Purchase"],
                    2
                ),

            # Risk
            "stockout_risk":
                summary["Stockout Risk"]

        }