import streamlit as st


def show_summary(summary):
    """
    Display the best forecasting model summary.
    """

    st.subheader("🏆 Best Forecasting Model")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Model",
        summary["Best Model"]
    )

    col2.metric(
        "RMSE",
        summary["RMSE"]
    )

    col3.metric(
        "MAE",
        summary["MAE"]
    )

    col4.metric(
        "R²",
        summary["R2"]
    )

    st.divider()