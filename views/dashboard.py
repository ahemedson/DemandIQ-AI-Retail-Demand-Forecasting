import streamlit as st

from utils.kpis import KPI
from utils.charts import Charts
from utils.business_insights import BusinessInsights
from utils.styling import style_plotly_figure


def show():

    # --------------------------------------------------
    # Check Dataset
    # --------------------------------------------------

    if st.session_state.dataset is None:
        st.title("📊 DemandIQ Dashboard")
        st.info("👈 Upload a retail dataset from the sidebar to begin.")
        return

    # --------------------------------------------------
    # Retrieve Shared Data
    # --------------------------------------------------

    clean_df = st.session_state.dataset
    loader = st.session_state.loader
    duplicates_removed = st.session_state.duplicates_removed

    # --------------------------------------------------
    # Initialize Objects
    # --------------------------------------------------

    kpi = KPI(clean_df)
    charts = Charts(clean_df)

    metrics = kpi.get_kpis()

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    st.title("📊 DemandIQ Dashboard")
    st.caption("AI-Powered Retail Analytics & Demand Forecasting Platform")

    # --------------------------------------------------
    # Business Overview
    # --------------------------------------------------

    st.subheader("📌 Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Total Sales",
        metrics["Total Sales"]
    )

    col2.metric(
        "🏪 Stores",
        metrics["Stores"]
    )

    col3.metric(
        "👥 Customers",
        metrics["Customers"]
    )

    col4.metric(
        "📅 Date Range",
        metrics["Date Range"]
    )

    # --------------------------------------------------
    # Daily Sales Trend
    # --------------------------------------------------

    st.divider()

    st.subheader("📈 Daily Sales Trend")

    st.plotly_chart(
        style_plotly_figure(charts.daily_sales_trend()),
        use_container_width=True
    )

    # --------------------------------------------------
    # Store & Weekday Analysis
    # --------------------------------------------------

    st.divider()

    left, right = st.columns(2)

    with left:

        st.plotly_chart(
            style_plotly_figure(charts.sales_by_store()),
            use_container_width=True
        )

    with right:

        st.plotly_chart(
            style_plotly_figure(charts.sales_by_day()),
            use_container_width=True
        )

    # --------------------------------------------------
    # Monthly Sales Trend
    # --------------------------------------------------

    st.divider()

    st.subheader("📅 Monthly Sales Trend")

    st.plotly_chart(
        style_plotly_figure(charts.monthly_sales_trend()),
        use_container_width=True
    )

    # --------------------------------------------------
    # Promotion Analysis
    # --------------------------------------------------

    st.divider()

    left, right = st.columns(2)

    with left:

        st.plotly_chart(
            style_plotly_figure(charts.promotion_impact()),
            use_container_width=True
        )

    with right:

        st.plotly_chart(
            style_plotly_figure(charts.sales_distribution()),
            use_container_width=True
        )

    # --------------------------------------------------
    # Store Performance
    # --------------------------------------------------

    st.divider()

    left, right = st.columns(2)

    with left:

        st.plotly_chart(
            style_plotly_figure(charts.top_stores()),
            use_container_width=True
        )

    with right:

        st.plotly_chart(
            style_plotly_figure(charts.bottom_stores()),
            use_container_width=True
        )

    # --------------------------------------------------
    # Business Insights
    # --------------------------------------------------

    st.divider()

    st.subheader("💡 Business Insights")

    insights = BusinessInsights(clean_df).generate()

    for insight in insights:

        st.success(insight)

    # --------------------------------------------------
    # Data Quality Summary
    # --------------------------------------------------

    st.divider()

    st.subheader("🧹 Data Quality Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Rows",
        f"{len(clean_df):,}"
    )

    col2.metric(
        "Missing Values",
        int(clean_df.isnull().sum().sum())
    )

    col3.metric(
        "Duplicates Removed",
        duplicates_removed
    )