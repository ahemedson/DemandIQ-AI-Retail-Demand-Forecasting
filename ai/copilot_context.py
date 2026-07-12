import streamlit as st
import pandas as pd

from config.settings import DATE_COLUMN


class CopilotContext:
    """
    Builds the business context supplied to the
    DemandIQ Copilot.

    Context Sources
    ---------------
    • Uploaded Dataset
    • Forecast Results
    • Inventory Summary
    """

    # --------------------------------------------------
    # Build Complete Context
    # --------------------------------------------------

    @classmethod
    def build(cls):

        sections = [

            cls.dataset_context(),

            cls.forecast_context(),

            cls.inventory_context()

        ]

        return "\n\n".join(

            section

            for section in sections

            if section

        )

    # --------------------------------------------------
    # Dataset Context
    # --------------------------------------------------

    @staticmethod
    def dataset_context():

        df = st.session_state.get("dataset")

        if df is None:

            return ""

        rows, cols = df.shape

        missing = int(df.isna().sum().sum())

        duplicates = int(df.duplicated().sum())

        numeric = list(

            df.select_dtypes(include="number").columns

        )

        categorical = list(

            df.select_dtypes(exclude="number").columns

        )

        context = [

            "# DATASET",

            f"Rows: {rows:,}",

            f"Columns: {cols}",

            f"Missing Values: {missing:,}",

            f"Duplicate Rows: {duplicates:,}",

            f"Column Names: {', '.join(df.columns)}",

            f"Numeric Columns: {', '.join(numeric)}",

            f"Categorical Columns: {', '.join(categorical)}"

        ]

        if DATE_COLUMN in df.columns:

            dates = pd.to_datetime(

                df[DATE_COLUMN]

            )

            context.append(

                f"Date Range: "

                f"{dates.min().date()} "

                f"to "

                f"{dates.max().date()}"

            )

        return "\n".join(context)

    # --------------------------------------------------
    # Forecast Context
    # --------------------------------------------------

    @staticmethod
    def forecast_context():

        forecast = st.session_state.get(

            "forecast_df"

        )

        service = st.session_state.get(

            "forecast_service"

        )

        if (

            forecast is None

            or

            service is None

        ):

            return ""

        model = service.best_model_summary()

        peak = forecast.loc[

            forecast["Forecast"].idxmax()

        ]

        low = forecast.loc[

            forecast["Forecast"].idxmin()

        ]

        return f"""
# FORECAST

Forecast Horizon:
{len(forecast)} Days

Forecast Period:
{forecast['Date'].min().date()} to {forecast['Date'].max().date()}

Total Forecast Sales:
{forecast['Forecast'].sum():,.0f}

Average Daily Sales:
{forecast['Forecast'].mean():,.0f}

Highest Forecast:
{peak['Forecast']:,.0f}

Peak Demand Date:
{peak['Date'].date()}

Lowest Forecast:
{low['Forecast']:,.0f}

Lowest Demand Date:
{low['Date'].date()}

Best Forecasting Model:
{model['Best Model']}

RMSE:
{model['RMSE']}

MAE:
{model['MAE']}

R²:
{model['R2']}
"""

    # --------------------------------------------------
    # Inventory Context
    # --------------------------------------------------

    @staticmethod
    def inventory_context():

        summary = st.session_state.get(

            "inventory_summary"

        )

        if summary is None:

            return ""

        interpretation = {

            "High":

                "Inventory should be replenished immediately to reduce stockout risk.",

            "Medium":

                "Inventory should be monitored closely.",

            "Low":

                "Current inventory appears sufficient."

        }.get(

            summary["Stockout Risk"],

            "Inventory status unavailable."

        )

        return f"""
# INVENTORY

Current Stock:
{summary['Current Stock']:,.0f}

Average Daily Demand:
{summary['Average Daily Demand']:,.0f}

Safety Stock:
{summary['Safety Stock']:,.0f}

Reorder Point:
{summary['Reorder Point']:,.0f}

Days of Inventory:
{summary['Days of Inventory']:.2f}

Stockout Risk:
{summary['Stockout Risk']}

Recommended Purchase:
{summary['Recommended Purchase']:,.0f}

Business Interpretation:
{interpretation}
"""