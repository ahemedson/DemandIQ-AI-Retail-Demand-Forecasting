import streamlit as st

from reports.report_service import ReportService


# ==================================================
# Session Initialization
# ==================================================

def initialize_session():

    if "report_service" not in st.session_state:

        st.session_state.report_service = ReportService()


# ==================================================
# Reports Page
# ==================================================

def show():

    initialize_session()

    st.title("📄 Executive Intelligence Report")

    st.caption(
        "Generate a professional executive report containing business insights, demand forecasts and inventory intelligence."
    )

    # ==================================================
    # Validate Dataset
    # ==================================================

    dataset = st.session_state.get("dataset")

    if dataset is None:

        st.info(
            "👈 Upload a retail dataset first."
        )

        return

    # ==================================================
    # Validate Forecast
    # ==================================================

    forecast_df = st.session_state.get(
        "forecast_df"
    )

    if forecast_df is None:

        st.warning(
            "Generate a demand forecast before creating the report."
        )

        return

    # ==================================================
    # Forecast Service
    # ==================================================

    forecast_service = st.session_state.get(
        "forecast_service"
    )

    if forecast_service is None:

        st.error(
            "Forecast service not available."
        )

        return

    model_summary = forecast_service.best_model_summary()

    inventory_summary = st.session_state.get(
        "inventory_summary"
    )

    ai_reports = {

        "forecast":

        st.session_state.get(

            "forecast_report"

        ),

        "inventory":

        st.session_state.get(

            "inventory_report"

        )

    }

    # ==================================================
    # Executive Overview
    # ==================================================

    st.subheader("Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(

            "Rows",

            f"{len(dataset):,}"

        )

    with col2:

        st.metric(

            "Forecast Days",

            len(forecast_df)

        )

    with col3:

        st.metric(

            "Forecast Model",

            model_summary.get(
                "Best Model",
                "-"
            )

        )

    with col4:

        if inventory_summary:

            st.metric(

                "Stockout Risk",

                inventory_summary.get(
                    "Stockout Risk",
                    "-"
                )

            )

        else:

            st.metric(

                "Stockout Risk",

                "N/A"

            )

    st.divider()

    # ==================================================
    # Included Sections
    # ==================================================

    with st.expander(

        "Report Contents",

        expanded=True

    ):

        st.markdown("""

### Executive Report Includes

- Executive Summary

- Executive Scorecard

- Dataset Overview

- Data Quality Assessment

- Business Performance

- Demand Forecast Analysis

- Forecast Model Evaluation

- Inventory Intelligence

- Business Risk Assessment

- AI Recommendations

- Executive Charts

- Appendix

""")

    st.divider()

        # ==================================================
    # Generate PDF
    # ==================================================

    if st.button(

        "📄 Generate Executive Report",

        type="primary",

        use_container_width=True

    ):

        figures = {}

        # ------------------------------------------
        # Forecast Chart
        # ------------------------------------------

        forecast_chart = st.session_state.get(

            "forecast_chart"

        )

        if forecast_chart is not None:

            figures["Demand Forecast"] = (

                forecast_chart

            )

        # ------------------------------------------
        # Inventory Chart
        # ------------------------------------------

        inventory_chart = st.session_state.get(

            "inventory_chart"

        )

        if inventory_chart is not None:

            figures["Inventory Projection"] = (

                inventory_chart

            )

        with st.spinner(

            "Generating Executive Intelligence Report..."

        ):

            result = (

                st.session_state

                .report_service

                .generate_pdf(

                    dataset=dataset,

                    forecast_df=forecast_df,

                    model_summary=model_summary,

                    inventory_summary=inventory_summary,

                    ai_reports=ai_reports,

                    figures=figures

                )

            )

        if not result["success"]:

            st.error(

                result["error"]

            )

            return

        st.success(

            "Executive report generated successfully."

        )

        st.download_button(

            label="⬇ Download Executive Report",

            data=result["pdf"],

            file_name="DemandIQ_Executive_Intelligence_Report.pdf",

            mime="application/pdf",

            use_container_width=True

        )

    st.divider()

    st.caption(

        "DemandIQ Reporting Engine v1.0"

    )