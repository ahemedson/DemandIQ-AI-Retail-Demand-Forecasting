import streamlit as st


class ForecastControls:
    """
    Forecast control panel.

    Returns
    -------
    dict

    {
        "forecast_days": int,
        "generate_forecast": bool
    }
    """

    FORECAST_OPTIONS = [
        7,
        30,
        90
    ]

    # --------------------------------------------------
    # Display Controls
    # --------------------------------------------------

    @classmethod
    def show(cls):

        st.subheader("⚙️ Forecast Controls")

        forecast_days = st.radio(

            "Forecast Horizon",

            options=cls.FORECAST_OPTIONS,

            horizontal=True,

            key="forecast_days"

        )

        generate_forecast = st.button(

            "📈 Generate Forecast",

            type="primary",

            use_container_width=True,

            key="generate_forecast"

        )

        st.divider()

        return {

            "forecast_days": forecast_days,

            "generate_forecast": generate_forecast

        }