import streamlit as st

from utils.formatter import Formatter


def show_kpis(summary):
    """
    Display executive inventory KPIs.
    """

    st.subheader("📊 Inventory Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Current Stock",
        Formatter.integer(summary["Current Stock"])
    )

    col2.metric(
        "Safety Stock",
        Formatter.integer(summary["Safety Stock"])
    )

    col3.metric(
        "Reorder Point",
        Formatter.integer(summary["Reorder Point"])
    )

    col4.metric(
        "Purchase Qty",
        Formatter.integer(summary["Recommended Purchase"])
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.metric(
            "Days of Inventory",
            f'{summary["Days of Inventory"]:.1f} Days'
        )

    with right:

        risk = summary["Stockout Risk"]

        if risk == "High":
            st.error(f"⚠ Stockout Risk: {risk}")

        elif risk == "Medium":
            st.warning(f"⚠ Stockout Risk: {risk}")

        else:
            st.success(f"✅ Stockout Risk: {risk}")

    st.divider()