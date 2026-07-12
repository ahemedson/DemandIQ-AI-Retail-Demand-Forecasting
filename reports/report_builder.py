from datetime import datetime

from reports.report_models import (
    ExecutiveReport,
    ReportMetadata
)

from reports.report_sections import ReportSections


class ReportBuilder:
    """
    Builds the complete Executive Intelligence Report.
    """

    VERSION = "1.0"

    def __init__(
        self,
        dataset=None,
        forecast_df=None,
        model_summary=None,
        inventory_summary=None,
        ai_reports=None
    ):

        self.dataset = dataset
        self.forecast_df = forecast_df
        self.model_summary = model_summary
        self.inventory_summary = inventory_summary
        self.ai_reports = ai_reports or {}

    # ==================================================
    # Build Report
    # ==================================================

    def build(self):

        metadata = self._metadata()

        sections = [

            # ------------------------------------------
            # Executive
            # ------------------------------------------

            ReportSections.executive_summary(

                self.dataset,

                self.forecast_df,

                self.model_summary,

                self.inventory_summary,

                self.ai_reports

            ),

            ReportSections.executive_scorecard(

                self.dataset,

                self.model_summary,

                self.inventory_summary

            ),

            ReportSections.executive_alerts(

                self.dataset,

                self.forecast_df,

                self.inventory_summary

            ),

            # ------------------------------------------
            # Dataset
            # ------------------------------------------

            ReportSections.dataset_overview(

                self.dataset

            ),

            ReportSections.data_quality(

                self.dataset

            ),

            # ------------------------------------------
            # Business
            # ------------------------------------------

            ReportSections.business_performance(

                self.forecast_df,

                self.model_summary,

                self.inventory_summary

            ),

            # ------------------------------------------
            # Forecasting
            # ------------------------------------------

            ReportSections.forecast_analysis(

                self.forecast_df,

                self.model_summary

            ),

            ReportSections.model_evaluation(

                self.model_summary

            ),

            # ------------------------------------------
            # Inventory
            # ------------------------------------------

            ReportSections.inventory_intelligence(

                self.inventory_summary

            ),

            # ------------------------------------------
            # Risks
            # ------------------------------------------

            ReportSections.business_risks(

                self.forecast_df,

                self.inventory_summary

            ),

            # ------------------------------------------
            # AI
            # ------------------------------------------

            ReportSections.ai_recommendations(

                self.ai_reports

            )

        ]

        return ExecutiveReport(

            metadata=metadata,

            sections=sections,

            properties={

                "dataset_rows": (
                    len(self.dataset)
                    if self.dataset is not None
                    else 0
                ),

                "forecast_days": (
                    len(self.forecast_df)
                    if self.forecast_df is not None
                    else 0
                )

            }

        )

    # ==================================================
    # Metadata
    # ==================================================

    def _metadata(self):

        return ReportMetadata(

            report_title="Executive Intelligence Report",

            generated_by="DemandIQ AI Business Analyst",

            generated_at=datetime.now().strftime(

                "%d %B %Y %H:%M"

            ),

            ai_model="Gemini 2.5 Flash",

            version=self.VERSION,

            company="DemandIQ",

            report_type="Retail Demand Forecasting Report"

        )