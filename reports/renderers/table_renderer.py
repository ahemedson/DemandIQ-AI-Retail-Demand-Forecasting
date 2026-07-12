from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch

from reportlab.platypus import (
    Paragraph,
    Table,
    TableStyle,
    Spacer
)


class TableRenderer:
    """
    Renders professional enterprise tables.
    """

    title_style = ParagraphStyle(

        "TableTitle",

        fontName="Helvetica-Bold",

        fontSize=14,

        leading=18,

        textColor=HexColor("#1E3A8A"),

        spaceAfter=10

    )

    header_style = ParagraphStyle(

        "Header",

        fontName="Helvetica-Bold",

        fontSize=9,

        alignment=TA_CENTER,

        textColor=colors.white

    )

    cell_style = ParagraphStyle(

        "Cell",

        fontName="Helvetica",

        fontSize=9,

        alignment=TA_LEFT,

        textColor=HexColor("#374151")

    )

    # ==================================================
    # Render
    # ==================================================

    @classmethod
    def render(
        cls,
        report_table
    ):

        story = []

        # ------------------------------------------
        # Title
        # ------------------------------------------

        story.append(

            Paragraph(

                report_table.title,

                cls.title_style

            )

        )

        # ------------------------------------------
        # Header
        # ------------------------------------------

        data = [[

            Paragraph(

                str(column),

                cls.header_style

            )

            for column in report_table.columns

        ]]

        # ------------------------------------------
        # Rows
        # ------------------------------------------

        for row in report_table.rows:

            formatted = []

            for value in row:

                formatted.append(

                    Paragraph(

                        str(value),

                        cls.cell_style

                    )

                )

            data.append(formatted)

        # ------------------------------------------
        # Auto Column Width
        # ------------------------------------------

        total_width = 6.4 * inch

        column_width = (

            total_width /

            max(

                len(report_table.columns),

                1

            )

        )

        col_widths = [

            column_width

        ] * len(report_table.columns)

        # ------------------------------------------
        # Build Table
        # ------------------------------------------

        table = Table(

            data,

            colWidths=col_widths,

            repeatRows=1

        )

        style = [

            (

                "BACKGROUND",

                (0, 0),

                (-1, 0),

                HexColor("#2563EB")

            ),

            (

                "TEXTCOLOR",

                (0, 0),

                (-1, 0),

                colors.white

            ),

            (

                "GRID",

                (0, 0),

                (-1, -1),

                0.5,

                HexColor("#CBD5E1")

            ),

            (

                "FONTNAME",

                (0, 0),

                (-1, 0),

                "Helvetica-Bold"

            ),

            (

                "ALIGN",

                (0, 0),

                (-1, -1),

                "CENTER"

            ),

            (

                "VALIGN",

                (0, 0),

                (-1, -1),

                "MIDDLE"

            ),

            (

                "TOPPADDING",

                (0, 0),

                (-1, -1),

                8

            ),

            (

                "BOTTOMPADDING",

                (0, 0),

                (-1, -1),

                8

            )

        ]

        # ------------------------------------------
        # Zebra Striping
        # ------------------------------------------

        for row in range(1, len(data)):

            if row % 2 == 0:

                style.append(

                    (

                        "BACKGROUND",

                        (0, row),

                        (-1, row),

                        HexColor("#F8FAFC")

                    )

                )

            else:

                style.append(

                    (

                        "BACKGROUND",

                        (0, row),

                        (-1, row),

                        colors.white

                    )

                )

        table.setStyle(

            TableStyle(style)

        )

        story.append(table)

        story.append(

            Spacer(

                1,

                0.25 * inch

            )

        )

        return story