import streamlit as st

from services.inventory_service import InventoryService
from ai.inventory_insights import InventoryInsights

from components.inventory_kpis import show_kpis
from components.inventory_chart import show_chart
from components.inventory_table import show_table
from components.analysis_panel import AnalysisPanel


# --------------------------------------------------
# Session Initialization
# --------------------------------------------------

def initialize_session():

    defaults = {

        "inventory_forecast": None,

        "inventory_summary": None,

        "inventory_report": None,

        "inventory_signature": None,

        "inventory_chart": None

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# --------------------------------------------------
# Inventory Intelligence Page
# --------------------------------------------------

def show():

    initialize_session()

    st.title("📦 Inventory Intelligence")

    st.caption(

        "Analyze inventory requirements using demand forecasts and AI-powered business recommendations."

    )

    # --------------------------------------------------
    # Dataset Check
    # --------------------------------------------------

    if st.session_state.dataset is None:

        st.info(

            "👈 Upload a retail dataset from the sidebar."

        )

        return

    # --------------------------------------------------
    # Forecast Check
    # --------------------------------------------------

    if (

        "forecast_service" not in st.session_state

        or

        st.session_state.forecast_service is None

    ):

        st.warning(

            "Please generate a forecast before using Inventory Intelligence."

        )

        return

    forecast_service = st.session_state.forecast_service

    # --------------------------------------------------
    # Inventory Settings
    # --------------------------------------------------

    st.sidebar.subheader(

        "📦 Inventory Settings"

    )

    current_stock = st.sidebar.number_input(

        "Current Stock",

        min_value=0,

        value=20000,

        step=100

    )

    lead_time = st.sidebar.slider(

        "Lead Time (Days)",

        min_value=1,

        max_value=30,

        value=7

    )

    service_level = st.sidebar.selectbox(

        "Service Level",

        [0.90, 0.95, 0.99],

        index=1

    )

    forecast_days = st.sidebar.selectbox(

        "Forecast Horizon",

        [7, 30, 90],

        index=1

    )

    generate_inventory = st.button(

        "📦 Generate Inventory Analysis",

        use_container_width=True,

        type="primary"

    )
        # --------------------------------------------------
    # Generate Inventory Analysis
    # --------------------------------------------------

    if generate_inventory:

        with st.spinner(

            "Generating inventory intelligence..."

        ):

            forecast = forecast_service.forecast(

                forecast_days

            )

            inventory_service = InventoryService(

                forecast_df=forecast,

                current_stock=current_stock,

                lead_time=lead_time,

                service_level=service_level

            )

            summary = inventory_service.get_summary()

            st.session_state.inventory_forecast = forecast

            st.session_state.inventory_summary = summary

            # Invalidate previous report
            st.session_state.inventory_report = None

            st.session_state.inventory_signature = {

                "forecast_days": forecast_days,

                "current_stock": current_stock,

                "lead_time": lead_time,

                "service_level": service_level

            }

        st.success(

            "Inventory analysis generated successfully."

        )

    # --------------------------------------------------
    # Wait Until Inventory Exists
    # --------------------------------------------------

    if st.session_state.inventory_summary is None:

        st.info(

            "Generate inventory analysis to continue."

        )

        return

    forecast = st.session_state.inventory_forecast

    summary = st.session_state.inventory_summary

    # --------------------------------------------------
    # Inventory KPIs
    # --------------------------------------------------

    show_kpis(

        summary

    )

    # --------------------------------------------------
    # Inventory Projection
    # --------------------------------------------------

    inventory_chart = show_chart(

        forecast,

        current_stock

    )

    st.session_state.inventory_chart = inventory_chart

    # --------------------------------------------------
    # Inventory Action Plan
    # --------------------------------------------------

    show_table(

        forecast,

        current_stock

    )

    st.divider()

        # --------------------------------------------------
    # Analysis Panel
    # --------------------------------------------------

    panel = AnalysisPanel.show(
        module="inventory"
    )

    current_signature = {

        "forecast_days": forecast_days,

        "current_stock": current_stock,

        "lead_time": lead_time,

        "service_level": service_level,

        "engine": panel["engine"],

        "analysis_type": panel["analysis_type"]

    }

    # --------------------------------------------------
    # Invalidate Cached Report
    # --------------------------------------------------

    if (

        st.session_state.inventory_signature

        !=

        current_signature

    ):

        st.session_state.inventory_report = None

        st.session_state.inventory_signature = None

    # --------------------------------------------------
    # Generate Analysis
    # --------------------------------------------------

    if panel["generate"]:

        with st.spinner(

            "Generating inventory business analysis..."

        ):

            report = InventoryInsights(

                summary

            ).generate(

                engine=panel["engine"],

                analysis_type=panel["analysis_type"]

            )

            st.session_state.inventory_report = report

    # --------------------------------------------------
    # Display Analysis
    # --------------------------------------------------

    report = st.session_state.inventory_report

    if report is None:

        st.info(

            "Select an analysis engine and click "

            "'Generate Analysis' to create inventory insights."

        )

        return

    st.subheader(

        "📄 Inventory Business Analysis"

    )

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