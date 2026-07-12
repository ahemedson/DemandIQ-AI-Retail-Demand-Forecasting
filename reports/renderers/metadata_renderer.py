from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

from reportlab.platypus import (
    Paragraph,
    Spacer
)


class MetadataRenderer:
    """
    Shared rendering utilities used across
    the Executive Intelligence Report.
    """

    styles = getSampleStyleSheet()

    # --------------------------------------------------
    # Initialize Styles
    # --------------------------------------------------

    heading_style = styles["Heading1"]
    heading_style.fontName = "Helvetica-Bold"
    heading_style.fontSize = 20
    heading_style.leading = 24
    heading_style.textColor = HexColor("#1E3A8A")
    heading_style.spaceAfter = 6
    heading_style.alignment = TA_LEFT

    subtitle_style = styles["Heading2"]
    subtitle_style.fontName = "Helvetica"
    subtitle_style.fontSize = 11
    subtitle_style.leading = 14
    subtitle_style.textColor = HexColor("#64748B")
    subtitle_style.spaceAfter = 18
    subtitle_style.alignment = TA_LEFT

    body_style = styles["BodyText"]
    body_style.fontName = "Helvetica"
    body_style.fontSize = 10.5
    body_style.leading = 18
    body_style.spaceAfter = 12
    body_style.textColor = HexColor("#374151")
    body_style.alignment = TA_LEFT

    # --------------------------------------------------
    # Section Heading
    # --------------------------------------------------

    @classmethod
    def section_heading(
        cls,
        title,
        subtitle=""
    ):

        elements = []

        elements.append(

            Paragraph(

                title,

                cls.heading_style

            )

        )

        if subtitle:

            elements.append(

                Paragraph(

                    subtitle,

                    cls.subtitle_style

                )

            )

        return elements

    # --------------------------------------------------
    # Paragraph
    # --------------------------------------------------

    @classmethod
    def paragraph(
        cls,
        text
    ):

        return [

            Paragraph(

                text,

                cls.body_style

            )

        ]

    # --------------------------------------------------
    # Spacer
    # --------------------------------------------------

    @staticmethod
    def spacer(height=0.20 * inch):

        return [

            Spacer(

                1,

                height

            )

        ]