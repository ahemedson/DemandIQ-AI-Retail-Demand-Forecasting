import streamlit as st

# -----------------------------
# Import Pages
# -----------------------------
from views import dashboard
from views import data_explorer
from views import forecasting
from views import inventory
from views import reports
from views import ai_copilot

# -----------------------------
# Session Manager
# -----------------------------
from utils.session_manager import (
    initialize_session,
    upload_dataset
)

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="DemandIQ",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session & Theme
# -----------------------------
initialize_session()

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# -----------------------------
# Sidebar & Upload
# -----------------------------
upload_dataset()

st.sidebar.divider()
st.session_state.dark_mode = st.sidebar.toggle(
    "🌙 Dark Mode",
    value=st.session_state.dark_mode
)

# -----------------------------
# Global Premium Styling
# -----------------------------
from utils.styling import apply_custom_styling
apply_custom_styling(dark_mode=st.session_state.dark_mode)

st.sidebar.divider()

# Navigation
page = st.sidebar.radio(

    "Navigation",

    [

        "📊 Dashboard",

        "🔍 Data Explorer",

        "📈 Demand Forecasting",

        "📦 Inventory Intelligence",

        "📄 Reports",

        "🤖 DemandIQ Copilot"

    ]

)

st.sidebar.divider()

# Show dataset status
if st.session_state.dataset is not None:
    st.sidebar.success("Dataset Ready")
    st.sidebar.write(f"Rows : {len(st.session_state.dataset):,}")
    st.sidebar.write(f"Columns : {len(st.session_state.dataset.columns)}")
else:
    st.sidebar.warning("No dataset uploaded")

# -----------------------------
# Routing
# -----------------------------
if page == "📊 Dashboard":
    dashboard.show()

elif page == "🔍 Data Explorer":
    data_explorer.show()

elif page == "📈 Demand Forecasting":
    forecasting.show()

elif page == "📦 Inventory Intelligence":
    inventory.show()

elif page == "📄 Reports":
    reports.show()

elif page == "🤖 DemandIQ Copilot":
    ai_copilot.show()