import streamlit as st
import pandas as pd

from utils.formatter import Formatter


def show_table(forecast_df, current_stock):
    """
    Display the inventory action plan.
    """

    st.subheader("📋 Inventory Action Plan")

    projection = forecast_df.copy()

    # ---------------------------------------
    # Calculate Remaining Stock
    # ---------------------------------------

    remaining_stock = []

    stock = current_stock

    for demand in projection["Forecast"]:

        stock -= demand

        remaining_stock.append(max(stock, 0))

    projection["Remaining Stock"] = remaining_stock

    # ---------------------------------------
    # Inventory Status
    # ---------------------------------------

    status = []

    for stock in remaining_stock:

        if stock <= 0:

            status.append("🔴 Stockout")

        elif stock < current_stock * 0.20:

            status.append("🟠 Critical")

        elif stock < current_stock * 0.40:

            status.append("🟡 Low Stock")

        else:

            status.append("🟢 Healthy")

    projection["Status"] = status

    # ---------------------------------------
    # Format Table
    # ---------------------------------------

    table = pd.DataFrame({

        "Date": projection["Date"].dt.strftime("%d %b %Y"),

        "Forecast": projection["Forecast"].round(0).astype(int),

        "Remaining Stock":
            projection["Remaining Stock"]
            .round(0)
            .astype(int),

        "Status": projection["Status"]

    })

    st.dataframe(

        table,

        use_container_width=True,

        hide_index=True

    )

    # ---------------------------------------
    # Download
    # ---------------------------------------

    csv = table.to_csv(index=False).encode("utf-8")

    st.download_button(

        "⬇ Download Inventory Report",

        csv,

        "inventory_action_plan.csv",

        "text/csv",

        use_container_width=True

    )

    st.divider()