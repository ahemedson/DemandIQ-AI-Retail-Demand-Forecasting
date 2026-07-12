from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch

from reportlab.platypus import (
    Image,
    Paragraph,
    Spacer,
)


class ChartRenderer:
    """
    Renders exported Plotly charts into the
    Executive Intelligence Report.
    """

    title_style = ParagraphStyle(

        "ChartTitle",

        fontName="Helvetica-Bold",

        fontSize=14,

        leading=18,

        alignment=TA_CENTER,

        textColor=HexColor("#1E3A8A"),

        spaceAfter=10

    )

    caption_style = ParagraphStyle(

        "Caption",

        fontName="Helvetica",

        fontSize=9,

        leading=12,

        alignment=TA_CENTER,

        textColor=HexColor("#64748B"),

        spaceAfter=14

    )

    # ==================================================
    # Render
    # ==================================================

    @classmethod
    def render(
        cls,
        chart
    ):

        story = []

        if not chart.image_path:

            return story

        image_path = Path(chart.image_path)

        if not image_path.exists():

            return story

        # ------------------------------------------
        # Title
        # ------------------------------------------

        story.append(

            Paragraph(

                chart.title,

                cls.title_style

            )

        )

        # ------------------------------------------
        # Image
        # ------------------------------------------

        image = Image(

            str(image_path)

        )

        image.drawWidth = 6.5 * inch

        image.drawHeight = 3.6 * inch

        story.append(image)

        # ------------------------------------------
        # Caption
        # ------------------------------------------

        story.append(

            Paragraph(

                "Figure: " + chart.title,

                cls.caption_style

            )

        )

        story.append(

            Spacer(

                1,

                0.30 * inch

            )

        )

        return story