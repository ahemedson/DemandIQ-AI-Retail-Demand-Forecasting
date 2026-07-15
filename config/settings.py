"""
DemandIQ Project Configuration
--------------------------------
Centralized configuration for the entire application.
"""

# ======================================================
# Dataset Configuration
# ======================================================

TARGET_COLUMN = "sales"

DATE_COLUMN = "date"

STORE_COLUMN = "store"


# ======================================================
# Forecast Configuration
# ======================================================

FORECAST_HORIZONS = [
    7,
    30,
    90
]


# ======================================================
# Machine Learning
# ======================================================

RANDOM_STATE = 42

TEST_SIZE = 0.20


# ======================================================
# Feature Columns
# ======================================================

FEATURE_COLUMNS = [

    "store",

    "dayofweek",

    "promo",

    "schoolholiday",

    "customers",

    "month",

    "week",

    "quarter",

    "is_weekend",

    "lag_1",

    "lag_7",

    "rolling_mean_7",

    "rolling_mean_30"

]


# ======================================================
# Random Forest Parameters
# ======================================================

RANDOM_FOREST_PARAMS = {

    "n_estimators": 200,

    "max_depth": 15,

    "random_state": RANDOM_STATE,

    "n_jobs": -1

}


# ======================================================
# XGBoost Parameters
# ======================================================

XGBOOST_PARAMS = {

    "n_estimators": 300,

    "learning_rate": 0.05,

    "max_depth": 8,

    "subsample": 0.8,

    "colsample_bytree": 0.8,

    "objective": "reg:squarederror",

    "random_state": RANDOM_STATE

}
    
# ==========================================================
# AI SETTINGS
# ==========================================================

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

AI_PROVIDER = "openrouter"

AI_MODEL = "google/gemini-2.5-flash"

AI_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Retrieve from Streamlit Secrets first (for cloud deployment), fallback to environment variables
try:
    secrets_keys = list(st.secrets.keys()) if hasattr(st, "secrets") else []
    print(f"DEBUG: Available Streamlit Secrets Keys: {secrets_keys}")
except Exception as e:
    print(f"DEBUG: Error listing secrets: {str(e)}")

if "OPENROUTER_API_KEY" in st.secrets:
    AI_API_KEY = st.secrets["OPENROUTER_API_KEY"]
else:
    AI_API_KEY = os.getenv("OPENROUTER_API_KEY")

AI_TEMPERATURE = 0.3

AI_MAX_TOKENS = 1000

AI_TIMEOUT = 60