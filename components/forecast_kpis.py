import streamlit as st


def show_kpis(forecast_df):
    """
    Display executive forecast KPIs.
    """

    if forecast_df.empty:

        return

    # ---------------------------------------
    # KPI Calculations
    # ---------------------------------------

    total_sales = forecast_df["Forecast"].sum()

    average_sales = forecast_df["Forecast"].mean()

    highest_sales = forecast_df["Forecast"].max()

    lowest_sales = forecast_df["Forecast"].min()

    highest_date = forecast_df.loc[
        forecast_df["Forecast"].idxmax(),
        "Date"
    ]

    lowest_date = forecast_df.loc[
        forecast_df["Forecast"].idxmin(),
        "Date"
    ]

    # ---------------------------------------
    # Display KPIs
    # ---------------------------------------

    st.subheader("📊 Forecast Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Forecast Sales",
        f"{total_sales:,.0f}"
    )

    col2.metric(
        "Average / Day",
        f"{average_sales:,.0f}"
    )

    col3.metric(
        "Highest Forecast",
        f"{highest_sales:,.0f}"
    )

    col4.metric(
        "Lowest Forecast",
        f"{lowest_sales:,.0f}"
    )

    st.info(
        f"""
**📅 Peak Demand:** {highest_date.strftime('%d %b %Y')}
({highest_sales:,.0f} sales)

**📉 Lowest Demand:** {lowest_date.strftime('%d %b %Y')}
({lowest_sales:,.0f} sales)
"""
    )

    st.divider()