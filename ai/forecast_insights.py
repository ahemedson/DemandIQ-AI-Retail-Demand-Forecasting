from ai.ai_report_generator import AIReportGenerator


class ForecastInsights:
    """
    Generates forecast analysis using the selected
    analysis engine.
    """

    def __init__(
        self,
        forecast_df,
        model_summary
    ):

        self.forecast_df = forecast_df
        self.model_summary = model_summary

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

            module="forecast",

            analysis_type=analysis_type,

            variables=self._prompt_variables(),

            fallback_data={

                "forecast": self.forecast_df,

                "model_summary": self.model_summary

            }

        )

    # --------------------------------------------------
    # Prompt Variables
    # --------------------------------------------------

    def _prompt_variables(self):

        forecast = self.forecast_df.copy()

        highest_idx = forecast["Forecast"].idxmax()
        lowest_idx = forecast["Forecast"].idxmin()

        return {

            # Forecast Period
            "forecast_days":
                len(forecast),

            "forecast_start":
                forecast["Date"].min().strftime("%d %b %Y"),

            "forecast_end":
                forecast["Date"].max().strftime("%d %b %Y"),

            # Sales Statistics
            "total_sales":
                round(
                    forecast["Forecast"].sum(),
                    2
                ),

            "average_sales":
                round(
                    forecast["Forecast"].mean(),
                    2
                ),

            "highest_sales":
                round(
                    forecast.loc[
                        highest_idx,
                        "Forecast"
                    ],
                    2
                ),

            "highest_date":
                forecast.loc[
                    highest_idx,
                    "Date"
                ].strftime("%d %b %Y"),

            "lowest_sales":
                round(
                    forecast.loc[
                        lowest_idx,
                        "Forecast"
                    ],
                    2
                ),

            "lowest_date":
                forecast.loc[
                    lowest_idx,
                    "Date"
                ].strftime("%d %b %Y"),

            # Model Performance
            "best_model":
                self.model_summary["Best Model"],

            "mae":
                round(
                    self.model_summary["MAE"],
                    2
                ),

            "rmse":
                round(
                    self.model_summary["RMSE"],
                    2
                ),

            "r2":
                round(
                    self.model_summary["R2"],
                    4
                )
        }