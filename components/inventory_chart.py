import streamlit as st
import plotly.graph_objects as go

from utils.formatter import Formatter


def show_chart(
    forecast_df,
    current_stock
):
    """
    Displays the projected inventory level based on
    forecasted demand.

    Returns
    -------
    plotly.graph_objects.Figure
        Plotly figure used by both the dashboard
        and the Executive Intelligence Report.
    """

    st.subheader("📈 Inventory Projection")

    # --------------------------------------------------
    # Validate Input
    # --------------------------------------------------

    if forecast_df is None:

        st.warning(
            "No inventory forecast available."
        )

        return None

    if forecast_df.empty:

        st.warning(
            "Forecast data is empty."
        )

        return None

    # --------------------------------------------------
    # Prepare Projection
    # --------------------------------------------------

    projection = forecast_df.copy()

    stock = float(current_stock)

    remaining_stock = []

    for demand in projection["Forecast"]:

        stock -= float(demand)

        remaining_stock.append(

            max(stock, 0)

        )

    projection["Remaining Stock"] = remaining_stock

    # --------------------------------------------------
    # Detect Stockout
    # --------------------------------------------------

    stockout_day = None

    for _, row in projection.iterrows():

        if row["Remaining Stock"] <= 0:

            stockout_day = row["Date"]

            break

    # --------------------------------------------------
    # Build Figure
    # --------------------------------------------------

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=projection["Date"],

            y=projection["Remaining Stock"],

            mode="lines+markers",

            name="Remaining Inventory",

            line=dict(

                width=3

            ),

            marker=dict(

                size=6

            ),

            hovertemplate=

            "<b>%{x}</b><br>"

            "Remaining Inventory: %{y:,.0f}"

            "<extra></extra>"

        )

    )

    # --------------------------------------------------
    # Stockout Marker
    # --------------------------------------------------

    if stockout_day is not None:

        fig.add_vline(

            x=stockout_day,

            line_dash="dash",

            line_width=2,

            annotation_text="Stockout",

            annotation_position="top"

        )

    # --------------------------------------------------
    # Layout
    # --------------------------------------------------

    fig.update_layout(

        title="Projected Inventory Level",

        template="plotly_white",

        hovermode="x unified",

        height=520,

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

        yaxis_title="Remaining Inventory"

    )

    # --------------------------------------------------
    # Display
    # --------------------------------------------------

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    # --------------------------------------------------
    # Inventory Status
    # --------------------------------------------------

    if stockout_day is None:

        st.success(

            "✅ Current inventory is sufficient for the selected forecast horizon."

        )

    else:

        st.error(

            f"⚠ Inventory is expected to run out around {Formatter.date(stockout_day)}."

        )

    st.divider()

    # --------------------------------------------------
    # Return Figure
    # --------------------------------------------------

    return fig