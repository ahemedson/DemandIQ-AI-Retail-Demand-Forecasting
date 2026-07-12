import streamlit as st
import pandas as pd


def show_model_comparison(results: pd.DataFrame):
    """
    Display model comparison results.
    """

    st.subheader("📊 Model Comparison")

    if results.empty:

        st.warning(
            "No model comparison available."
        )

        return

    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True
    )

    st.divider()