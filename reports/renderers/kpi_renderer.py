from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch

from reportlab.platypus import (
    Paragraph,
    Table,
    TableStyle,
    Spacer
)


class KPIRenderer:
    """
    Renders executive KPI cards.
    """

    title_style = ParagraphStyle(

        "KPI Title",

        fontName="Helvetica",

        fontSize=10,

        leading=12,

        alignment=TA_CENTER,

        textColor=HexColor("#64748B")

    )

    value_style = ParagraphStyle(

        "KPI Value",

        fontName="Helvetica-Bold",

        fontSize=20,

        leading=24,

        alignment=TA_CENTER,

        textColor=HexColor("#1E3A8A")

    )

    status_style = ParagraphStyle(

        "KPI Status",

        fontName="Helvetica-Bold",

        fontSize=9,

        leading=12,

        alignment=TA_CENTER,

        textColor=HexColor("#059669")

    )

    # --------------------------------------------------
    # Render
    # --------------------------------------------------

    @classmethod
    def render(
        cls,
        kpis
    ):

        story = []

        if not kpis:

            return story

        rows = []

        current_row = []

        for kpi in kpis:

            card = cls._card(kpi)

            current_row.append(card)

            if len(current_row) == 2:

                rows.append(current_row)

                current_row = []

        if current_row:

            while len(current_row) < 2:

                current_row.append("")

            rows.append(current_row)

        table = Table(

            rows,

            colWidths=[3.2 * inch, 3.2 * inch],

            hAlign="CENTER"

        )

        table.setStyle(

            TableStyle([

                (

                    "BOTTOMPADDING",

                    (0, 0),

                    (-1, -1),

                    12

                ),

                (

                    "TOPPADDING",

                    (0, 0),

                    (-1, -1),

                    12

                ),

                (

                    "VALIGN",

                    (0, 0),

                    (-1, -1),

                    "TOP"

                )

            ])

        )

        story.append(table)

        story.append(

            Spacer(

                1,

                0.25 * inch

            )

        )

        return story

    # --------------------------------------------------
    # KPI Card
    # --------------------------------------------------

    @classmethod
    def _card(
        cls,
        kpi
    ):

        content = [

            [

                Paragraph(

                    kpi.title,

                    cls.title_style

                )

            ],

            [

                Paragraph(

                    str(kpi.value),

                    cls.value_style

                )

            ]

        ]

        if getattr(kpi, "status", None):

            content.append(

                [

                    Paragraph(

                        kpi.status,

                        cls.status_style

                    )

                ]

            )

        card = Table(

            content,

            colWidths=[2.9 * inch]

        )

        card.setStyle(

            TableStyle([

                (

                    "BACKGROUND",

                    (0, 0),

                    (-1, -1),

                    HexColor("#F8FAFC")

                ),

                (

                    "BOX",

                    (0, 0),

                    (-1, -1),

                    1,

                    HexColor("#CBD5E1")

                ),

                (

                    "LINEBEFORE",

                    (0, 0),

                    (0, -1),

                    5,

                    HexColor("#2563EB")

                ),

                (

                    "TOPPADDING",

                    (0, 0),

                    (-1, -1),

                    12

                ),

                (

                    "BOTTOMPADDING",

                    (0, 0),

                    (-1, -1),

                    12

                ),

                (

                    "LEFTPADDING",

                    (0, 0),

                    (-1, -1),

                    12

                ),

                (

                    "RIGHTPADDING",

                    (0, 0),

                    (-1, -1),

                    12

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

                )

            ])

        )

        return card