from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch

from reportlab.platypus import (
    Paragraph,
    Table,
    TableStyle,
    Spacer
)


class ScoreRenderer:
    """
    Renders executive business scorecards.
    """

    title_style = ParagraphStyle(

        "ScoreTitle",

        fontName="Helvetica-Bold",

        fontSize=12,

        alignment=TA_CENTER,

        textColor=HexColor("#1E293B")

    )

    score_style = ParagraphStyle(

        "ScoreValue",

        fontName="Helvetica-Bold",

        fontSize=24,

        alignment=TA_CENTER,

        textColor=HexColor("#2563EB")

    )

    grade_style = ParagraphStyle(

        "Grade",

        fontName="Helvetica-Bold",

        fontSize=16,

        alignment=TA_CENTER,

        textColor=HexColor("#FFFFFF")

    )

    description_style = ParagraphStyle(

        "Description",

        fontName="Helvetica",

        fontSize=9,

        leading=12,

        alignment=TA_CENTER,

        textColor=HexColor("#475569")

    )

    # --------------------------------------------------
    # Render
    # --------------------------------------------------

    @classmethod
    def render(
        cls,
        scores
    ):

        story = []

        if not scores:

            return story

        rows = []
        current = []

        for score in scores:

            current.append(

                cls._card(score)

            )

            if len(current) == 2:

                rows.append(current)

                current = []

        if current:

            while len(current) < 2:

                current.append("")

            rows.append(current)

        table = Table(

            rows,

            colWidths=[3.2 * inch, 3.2 * inch],

            hAlign="CENTER"

        )

        table.setStyle(

            TableStyle([

                ("BOTTOMPADDING", (0,0), (-1,-1), 12),

                ("TOPPADDING", (0,0), (-1,-1), 12),

                ("VALIGN", (0,0), (-1,-1), "TOP")

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
    # Individual Card
    # --------------------------------------------------

    @classmethod
    def _card(
        cls,
        score
    ):

        grade_colour = {

            "A": "#16A34A",

            "B": "#22C55E",

            "C": "#EAB308",

            "D": "#F97316",

            "F": "#DC2626"

        }.get(

            score.grade,

            "#2563EB"

        )

        badge = Table(

            [[

                Paragraph(

                    score.grade,

                    cls.grade_style

                )

            ]],

            colWidths=[0.55 * inch],

            rowHeights=[0.38 * inch]

        )

        badge.setStyle(

            TableStyle([

                (

                    "BACKGROUND",

                    (0,0),

                    (-1,-1),

                    HexColor(grade_colour)

                ),

                (

                    "ALIGN",

                    (0,0),

                    (-1,-1),

                    "CENTER"

                ),

                (

                    "VALIGN",

                    (0,0),

                    (-1,-1),

                    "MIDDLE"

                ),

                (

                    "BOX",

                    (0,0),

                    (-1,-1),

                    0,

                    HexColor(grade_colour)

                )

            ])

        )

        content = [

            [

                Paragraph(

                    score.title,

                    cls.title_style

                )

            ],

            [

                Paragraph(

                    f"{score.score:.1f}",

                    cls.score_style

                )

            ],

            [

                badge

            ],

            [

                Paragraph(

                    score.description,

                    cls.description_style

                )

            ]

        ]

        card = Table(

            content,

            colWidths=[2.9 * inch]

        )

        card.setStyle(

            TableStyle([

                (

                    "BACKGROUND",

                    (0,0),

                    (-1,-1),

                    HexColor("#FFFFFF")

                ),

                (

                    "BOX",

                    (0,0),

                    (-1,-1),

                    1,

                    HexColor("#CBD5E1")

                ),

                (

                    "LINEBEFORE",

                    (0,0),

                    (0,-1),

                    5,

                    HexColor("#2563EB")

                ),

                (

                    "TOPPADDING",

                    (0,0),

                    (-1,-1),

                    12

                ),

                (

                    "BOTTOMPADDING",

                    (0,0),

                    (-1,-1),

                    12

                ),

                (

                    "LEFTPADDING",

                    (0,0),

                    (-1,-1),

                    12

                ),

                (

                    "RIGHTPADDING",

                    (0,0),

                    (-1,-1),

                    12

                ),

                (

                    "ALIGN",

                    (0,0),

                    (-1,-1),

                    "CENTER"

                ),

                (

                    "VALIGN",

                    (0,0),

                    (-1,-1),

                    "MIDDLE"

                )

            ])

        )

        return card