from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch

from reportlab.platypus import (
    Paragraph,
    Table,
    TableStyle,
    Spacer
)


class AlertRenderer:
    """
    Renders executive business alerts.
    """

    title_style = ParagraphStyle(

        "AlertTitle",

        fontName="Helvetica-Bold",

        fontSize=12,

        leading=16,

        alignment=TA_LEFT,

        textColor=HexColor("#111827")

    )

    description_style = ParagraphStyle(

        "AlertDescription",

        fontName="Helvetica",

        fontSize=10,

        leading=16,

        alignment=TA_LEFT,

        textColor=HexColor("#374151")

    )

    LEVELS = {

        "High": {

            "background": HexColor("#FEE2E2"),

            "border": HexColor("#DC2626")

        },

        "Medium": {

            "background": HexColor("#FEF3C7"),

            "border": HexColor("#D97706")

        },

        "Low": {

            "background": HexColor("#DCFCE7"),

            "border": HexColor("#16A34A")

        }

    }

    # ==================================================
    # Render
    # ==================================================

    @classmethod
    def render(

        cls,

        alerts

    ):

        story = []

        if not alerts:

            return story

        for alert in alerts:

            story.append(

                cls._alert_card(

                    alert

                )

            )

            story.append(

                Spacer(

                    1,

                    0.12 * inch

                )

            )

        story.append(

            Spacer(

                1,

                0.18 * inch

            )

        )

        return story

    # ==================================================
    # Individual Alert
    # ==================================================

    @classmethod
    def _alert_card(

        cls,

        alert

    ):

        style = cls.LEVELS.get(

            alert.level,

            cls.LEVELS["Low"]

        )

        title = Paragraph(

            f"<b>{alert.level} Priority</b> • {alert.title}",

            cls.title_style

        )

        description = Paragraph(

            alert.description,

            cls.description_style

        )

        table = Table(

            [

                [title],

                [description]

            ],

            colWidths=[6.25 * inch]

        )

        table.setStyle(

            TableStyle([

                (

                    "BACKGROUND",

                    (0, 0),

                    (-1, -1),

                    style["background"]

                ),

                (

                    "LINEBEFORE",

                    (0, 0),

                    (0, -1),

                    6,

                    style["border"]

                ),

                (

                    "BOX",

                    (0, 0),

                    (-1, -1),

                    0.5,

                    HexColor("#CBD5E1")

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

                    14

                ),

                (

                    "RIGHTPADDING",

                    (0, 0),

                    (-1, -1),

                    14

                ),

                (

                    "VALIGN",

                    (0, 0),

                    (-1, -1),

                    "TOP"

                )

            ])

        )

        return table