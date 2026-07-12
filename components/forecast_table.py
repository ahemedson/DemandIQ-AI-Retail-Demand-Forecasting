import streamlit as st
import pandas as pd

from utils.formatter import Formatter


def show_table(forecast_df: pd.DataFrame):
    """
    Display forecast results in a table with
    download functionality.
    """

    st.subheader("📋 Forecast Results")

    if forecast_df.empty:

        st.warning(
            "No forecast available."
        )

        return

    # ---------------------------------------
    # Format Table
    # ---------------------------------------

    table = forecast_df.copy()

    table["Date"] = table["Date"].apply(
        Formatter.date
    )

    table["Forecast"] = table["Forecast"].round(2)

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )

    # ---------------------------------------
    # Download Forecast
    # ---------------------------------------

    csv = forecast_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇ Download Forecast CSV",
        data=csv,
        file_name="forecast.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.divider()