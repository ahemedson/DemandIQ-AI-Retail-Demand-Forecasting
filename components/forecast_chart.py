import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from config.settings import (
    DATE_COLUMN,
    TARGET_COLUMN
)


def show_chart(
    history_df,
    forecast_df
):
    """
    Displays historical sales together with the generated
    demand forecast.

    Returns
    -------
    plotly.graph_objects.Figure
        Plotly figure used both in Streamlit and the
        Executive Intelligence Report.
    """

    st.subheader("📈 Sales Forecast")

    # --------------------------------------------------
    # Validate Inputs
    # --------------------------------------------------

    if history_df is None or forecast_df is None:

        st.warning(
            "No forecast available."
        )

        return None

    if history_df.empty or forecast_df.empty:

        st.warning(
            "Forecast data is empty."
        )

        return None

    # --------------------------------------------------
    # Historical Data
    # --------------------------------------------------

    history = history_df.copy()

    history = history.sort_values(
        DATE_COLUMN
    )

    history = history.tail(60)

    # --------------------------------------------------
    # Forecast Data
    # --------------------------------------------------

    chart_forecast = forecast_df.copy()

    last_row = pd.DataFrame({

        "Date": [

            history.iloc[-1][DATE_COLUMN]

        ],

        "Forecast": [

            history.iloc[-1][TARGET_COLUMN]

        ]

    })

    chart_forecast = pd.concat(

        [

            last_row,

            chart_forecast

        ],

        ignore_index=True

    )

    chart_forecast = chart_forecast.sort_values(

        "Date"

    )

    # --------------------------------------------------
    # Build Figure
    # --------------------------------------------------

    fig = go.Figure()

    # Historical Sales

    fig.add_trace(

        go.Scatter(

            x=history[DATE_COLUMN],

            y=history[TARGET_COLUMN],

            mode="lines",

            name="Historical Sales",

            line=dict(

                width=3

            ),

            hovertemplate=

            "<b>%{x}</b><br>"

            "Historical Sales: %{y:,.0f}"

            "<extra></extra>"

        )

    )

    # Forecast

    fig.add_trace(

        go.Scatter(

            x=chart_forecast["Date"],

            y=chart_forecast["Forecast"],

            mode="lines+markers",

            name="Forecast",

            line=dict(

                width=3,

                dash="dash"

            ),

            marker=dict(

                size=6

            ),

            hovertemplate=

            "<b>%{x}</b><br>"

            "Forecast: %{y:,.0f}"

            "<extra></extra>"

        )

    )

    # --------------------------------------------------
    # Forecast Boundary
    # --------------------------------------------------

    fig.add_vline(

        x=forecast_df.iloc[0]["Date"],

        line_dash="dot",

        line_width=2,

        annotation_text="Forecast Starts",

        annotation_position="top"

    )

    # --------------------------------------------------
    # Layout
    # --------------------------------------------------

    fig.update_layout(

        title="Historical Sales vs Forecast",

        template="plotly_white",

        hovermode="x unified",

        height=550,

        margin=dict(

            l=20,

            r=20,

            t=70,

            b=20

        ),

        legend=dict(

            orientation="h",

            y=1.08,

            x=1,

            xanchor="right"

        ),

        xaxis_title="Date",

        yaxis_title="Sales"

    )

    # --------------------------------------------------
    # Display
    # --------------------------------------------------

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # --------------------------------------------------
    # Return Figure
    # --------------------------------------------------

    return fig