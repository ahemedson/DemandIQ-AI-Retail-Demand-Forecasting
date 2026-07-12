from reportlab.lib.units import inch

from reports.renderers.cover_renderer import CoverRenderer
from reports.renderers.metadata_renderer import MetadataRenderer
from reports.renderers.kpi_renderer import KPIRenderer
from reports.renderers.score_renderer import ScoreRenderer
from reports.renderers.alert_renderer import AlertRenderer
from reports.renderers.table_renderer import TableRenderer
from reports.renderers.chart_renderer import ChartRenderer


class ReportRenderer:
    """
    Converts an ExecutiveReport into ReportLab Flowables.

    This class does not generate the PDF directly.
    Instead, it builds a list of ReportLab elements
    that are later consumed by PDFGenerator.
    """

    def __init__(self):

        self.story = []

    # ==================================================
    # Public API
    # ==================================================

    def render(self, report):

        self.story = []

        # ------------------------------------------
        # Cover Page
        # ------------------------------------------

        self.story.extend(

            CoverRenderer.render(

                report.metadata

            )

        )

        # ------------------------------------------
        # Sections
        # ------------------------------------------

        for section in report.sections:

            self.story.extend(

                self._section(

                    section

                )

            )

        return self.story

    # ==================================================
    # Render One Section
    # ==================================================

    def _section(self, section):

        elements = []

        elements.extend(

            MetadataRenderer.section_heading(

                section.title,

                section.subtitle

            )

        )

        if section.content:

            elements.extend(

                MetadataRenderer.paragraph(

                    section.content

                )

            )

        if section.kpis:

            elements.extend(

                KPIRenderer.render(

                    section.kpis

                )

            )

        if section.scores:

            elements.extend(

                ScoreRenderer.render(

                    section.scores

                )

            )

        if section.alerts:

            elements.extend(

                AlertRenderer.render(

                    section.alerts

                )

            )

        if section.tables:

            for table in section.tables:

                elements.extend(

                    TableRenderer.render(

                        table

                    )

                )

        if section.charts:

            for chart in section.charts:

                elements.extend(

                    ChartRenderer.render(

                        chart

                    )

                )

        elements.extend(

            MetadataRenderer.spacer(

                0.30 * inch

            )

        )

        return elements