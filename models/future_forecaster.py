import pandas as pd

from config.settings import (
    DATE_COLUMN,
    TARGET_COLUMN
)

from models.forecast_feature_builder import ForecastFeatureBuilder


class FutureForecaster:
    """
    Generates recursive future forecasts using a
    trained machine learning model.
    """

    def __init__(self, model, history):

        self.model = model
        self.history = history.copy()

    # --------------------------------------------------
    # Generate Future Dates
    # --------------------------------------------------

    def generate_future_dates(self, days):

        last_date = self.history[DATE_COLUMN].max()

        return pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=days,
            freq="D"
        )

    # --------------------------------------------------
    # Update History
    # --------------------------------------------------

    def update_history(self, future_date, prediction):

        latest = self.history.iloc[-1].copy()

        latest[DATE_COLUMN] = future_date
        latest[TARGET_COLUMN] = prediction

        self.history = pd.concat(
            [
                self.history,
                pd.DataFrame([latest])
            ],
            ignore_index=True
        )

    # --------------------------------------------------
    # Forecast
    # --------------------------------------------------

    def forecast(self, days):

        future_dates = self.generate_future_dates(days)

        builder = ForecastFeatureBuilder(self.history)

        forecasts = []

        for future_date in future_dates:

            features = builder.build(future_date)

            prediction = float(
                self.model.predict(features)[0]
            )

            forecasts.append({

                "Date": future_date,

                "Forecast": prediction

            })

            self.update_history(
                future_date,
                prediction
            )

            builder.history = self.history

        return pd.DataFrame(forecasts)