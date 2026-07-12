from io import BytesIO

from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    PageBreak
)

from reports.report_renderer import ReportRenderer


class PDFGenerator:
    """
    Generates the Executive Intelligence Report.

    Responsibilities
    ----------------
    • Build ReportLab document
    • Render report sections
    • Add page numbers
    • Return PDF as BytesIO
    """

    PAGE_MARGIN = 0.6 * inch

    def __init__(self):

        self.renderer = ReportRenderer()

    # ==================================================
    # Generate PDF
    # ==================================================

    def generate(
        self,
        report
    ):

        pdf = BytesIO()

        document = SimpleDocTemplate(

            pdf,

            pagesize=(8.27 * inch, 11.69 * inch),   # A4

            leftMargin=self.PAGE_MARGIN,

            rightMargin=self.PAGE_MARGIN,

            topMargin=self.PAGE_MARGIN,

            bottomMargin=self.PAGE_MARGIN

        )

        story = self.renderer.render(

            report

        )

        document.build(

            story,

            onFirstPage=self._first_page,

            onLaterPages=self._later_pages

        )

        pdf.seek(0)

        return pdf

    # ==================================================
    # First Page
    # ==================================================

    @staticmethod
    def _first_page(

        canvas,

        document

    ):

        PDFGenerator._page_border(

            canvas,

            document

        )

    # ==================================================
    # Remaining Pages
    # ==================================================

    @staticmethod
    def _later_pages(

        canvas,

        document

    ):

        PDFGenerator._page_border(

            canvas,

            document

        )

        PDFGenerator._page_footer(

            canvas,

            document

        )

    # ==================================================
    # Border
    # ==================================================

    @staticmethod
    def _page_border(

        canvas,

        document

    ):

        width, height = document.pagesize

        canvas.saveState()

        canvas.setStrokeColor(

            HexColor("#CBD5E1")

        )

        canvas.setLineWidth(

            0.5

        )

        canvas.rect(

            0.35 * inch,

            0.35 * inch,

            width - 0.70 * inch,

            height - 0.70 * inch

        )

        canvas.restoreState()

    # ==================================================
    # Footer
    # ==================================================

    @staticmethod
    def _page_footer(

        canvas,

        document

    ):

        width, _ = document.pagesize

        canvas.saveState()

        canvas.setFont(

            "Helvetica",

            9

        )

        canvas.setFillColor(

            HexColor("#64748B")

        )

        canvas.drawString(

            0.60 * inch,

            0.45 * inch,

            "DemandIQ Executive Intelligence Report"

        )

        canvas.drawRightString(

            width - 0.60 * inch,

            0.45 * inch,

            f"Page {document.page}"

        )

        canvas.restoreState()