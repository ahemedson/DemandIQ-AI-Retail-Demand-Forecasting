import streamlit as st

from services.forecasting_service import ForecastingService

from ai.forecast_insights import ForecastInsights

from components.forecast_summary import show_summary
from components.model_comparison import show_model_comparison
from components.forecast_kpis import show_kpis
from components.forecast_chart import show_chart
from components.forecast_table import show_table

from components.forecast_controls import ForecastControls
from components.analysis_panel import AnalysisPanel


# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------

def initialize_session():

    defaults = {

        "forecast_service": None,

        "forecast_df": None,

        "forecast_report": None,

        "forecast_signature": None,

        "forecast_chart": None

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value

# --------------------------------------------------
# Forecasting Page
# --------------------------------------------------

def show():

    initialize_session()

    st.title("📈 Demand Forecasting")

    st.caption(
        "Generate machine learning forecasts and AI-powered business insights."
    )

    # --------------------------------------------------
    # Dataset Check
    # --------------------------------------------------

    if st.session_state.dataset is None:

        st.info(
            "👈 Upload a retail dataset from the sidebar."
        )

        return

    dataset = st.session_state.dataset

    # --------------------------------------------------
    # Forecast Service
    # --------------------------------------------------

    if (

        st.session_state.forecast_service is None

        or

        st.session_state.forecast_service.df is not dataset

    ):

        with st.spinner(
            "Initializing forecasting engine..."
        ):

            st.session_state.forecast_service = (

                ForecastingService(dataset)

            )

            st.session_state.forecast_df = None

            st.session_state.forecast_report = None

            st.session_state.forecast_signature = None

    service = st.session_state.forecast_service

    # --------------------------------------------------
    # Train Models
    # --------------------------------------------------

    if not service.is_trained():

        with st.spinner(
            "Training forecasting models..."
        ):

            service.train()

    # --------------------------------------------------
    # Best Model Summary
    # --------------------------------------------------

    summary = service.best_model_summary()

    show_summary(summary)

    # --------------------------------------------------
    # Model Comparison
    # --------------------------------------------------

    comparison = service.model_comparison()

    show_model_comparison(comparison)

        # --------------------------------------------------
    # Forecast Controls
    # --------------------------------------------------

    controls = ForecastControls.show()

    forecast_days = controls["forecast_days"]

    generate_forecast = controls["generate_forecast"]

    # --------------------------------------------------
    # Generate Forecast
    # --------------------------------------------------

    if generate_forecast:

        with st.spinner(
            f"Generating {forecast_days}-day forecast..."
        ):

            forecast = service.forecast(
                forecast_days
            )

            st.session_state.forecast_df = forecast

            # Invalidate previous analysis
            st.session_state.forecast_report = None

            st.session_state.forecast_signature = None

        st.success(
            f"Successfully generated a {forecast_days}-day forecast."
        )

    # --------------------------------------------------
    # Forecast Availability Check
    # --------------------------------------------------

    forecast = st.session_state.forecast_df

    if forecast is None:

        st.info(
            "Generate a forecast to view results and business analysis."
        )

        return

    # --------------------------------------------------
    # Forecast KPIs
    # --------------------------------------------------

    show_kpis(
        forecast
    )

    # --------------------------------------------------
    # Forecast Chart
    # --------------------------------------------------

    show_chart(

        history_df=dataset,

        forecast_df=forecast

    )

    # --------------------------------------------------
    # Forecast Table
    # --------------------------------------------------

    show_table(
        forecast
    )

        # --------------------------------------------------
    # Analysis Panel
    # --------------------------------------------------

    panel = AnalysisPanel.show(
        module="forecast"
    )

    current_signature = {

        "forecast_days": forecast_days,

        "engine": panel["engine"],

        "analysis_type": panel["analysis_type"]

    }

    # --------------------------------------------------
    # Invalidate Cached Report
    # --------------------------------------------------

    if (

        st.session_state.forecast_signature

        !=

        current_signature

    ):

        st.session_state.forecast_report = None

        st.session_state.forecast_signature = (

            current_signature

        )

    # --------------------------------------------------
    # Generate Analysis
    # --------------------------------------------------

    if panel["generate"]:

        with st.spinner(
            "Generating business analysis..."
        ):

            report = ForecastInsights(

                forecast_df=forecast,

                model_summary=summary

            ).generate(

                engine=panel["engine"],

                analysis_type=panel["analysis_type"]

            )

            st.session_state.forecast_report = report

    # --------------------------------------------------
    # Display Analysis
    # --------------------------------------------------

    report = st.session_state.forecast_report

    if report is None:

        st.info(

            "Select an analysis engine and click "

            "'Generate Analysis' to create business insights."

        )

        return

    st.divider()

    st.subheader("📄 Business Analysis")

    if report["engine"] == "AI":

        st.success(
            "🤖 Generated using AI Business Analyst"
        )

    else:

        st.info(
            "📋 Generated using Business Rules Engine"
        )

    if report.get("title"):

        st.markdown(

            f"### {report['title']}"

        )

    st.markdown(

        report["content"]

    )

    metadata = report.get(

        "metadata",

        {}

    )

    if metadata:

        with st.expander(

            "Analysis Details"

        ):

            if "generated_at" in metadata:

                st.write(

                    "**Generated:**",

                    metadata["generated_at"]

                )

            if "model" in metadata:

                st.write(

                    "**Model:**",

                    metadata["model"]

                )

            if "usage" in metadata:

                usage = metadata["usage"]

                st.write(

                    "**Prompt Tokens:**",

                    usage.get(

                        "prompt_tokens",

                        0

                    )

                )

                st.write(

                    "**Completion Tokens:**",

                    usage.get(

                        "completion_tokens",

                        0

                    )

                )

                st.write(

                    "**Total Tokens:**",

                    usage.get(

                        "total_tokens",

                        0

                    )

                )

            if "rule_version" in metadata:

                st.write(

                    "**Rule Version:**",

                    metadata["rule_version"]

                )