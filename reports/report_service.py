from pathlib import Path

from reports.chart_exporter import ChartExporter
from reports.pdf_generator import PDFGenerator
from reports.report_builder import ReportBuilder


class ReportService:
    """
    Generates the Executive Intelligence Report.

    Responsibilities
    ----------------
    • Export Plotly charts
    • Build report object
    • Attach exported chart images
    • Generate PDF
    """

    def __init__(self):

        self.chart_exporter = ChartExporter()

        self.pdf_generator = PDFGenerator()

    # ==================================================
    # Generate PDF
    # ==================================================

    def generate_pdf(
        self,
        dataset,
        forecast_df,
        model_summary,
        inventory_summary,
        ai_reports,
        figures=None
    ):

        figures = figures or {}

        try:

            # ------------------------------------------
            # Export Charts
            # ------------------------------------------

            exported_charts = {}

            if figures:

                exported_charts = (

                    self.chart_exporter.export_all(

                        figures

                    )

                )

            # ------------------------------------------
            # Build Report
            # ------------------------------------------

            report = ReportBuilder(

                dataset=dataset,

                forecast_df=forecast_df,

                model_summary=model_summary,

                inventory_summary=inventory_summary,

                ai_reports=ai_reports

            ).build()

            # ------------------------------------------
            # Build Chart Lookup
            # ------------------------------------------

            chart_lookup = {

                Path(path).stem: path

                for path in exported_charts.values()

            }

            # ------------------------------------------
            # Attach Charts
            # ------------------------------------------

            for section in report.sections:

                for chart in section.charts:

                    image_path = chart_lookup.get(

                        chart.title

                    )

                    if image_path:

                        chart.image_path = image_path

            # ------------------------------------------
            # Generate PDF
            # ------------------------------------------

            pdf_buffer = self.pdf_generator.generate(

                report

            )

            return {

                "success": True,

                "pdf": pdf_buffer,

                "report": report

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

        finally:

            self.chart_exporter.cleanup()