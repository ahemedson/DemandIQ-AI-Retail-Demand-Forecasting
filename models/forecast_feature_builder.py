import pandas as pd

from config.settings import (
    DATE_COLUMN,
    STORE_COLUMN,
    TARGET_COLUMN,
    FEATURE_COLUMNS
)


class ForecastFeatureBuilder:
    """
    Builds the feature vector for a single future prediction.
    The output schema always matches FEATURE_COLUMNS exactly.
    """

    def __init__(self, history):

        self.history = history.copy()

    # --------------------------------------------------
    # Build Features
    # --------------------------------------------------

    def build(self, future_date):

        history = self.history.sort_values(
            [STORE_COLUMN, DATE_COLUMN]
        )

        latest = history.iloc[-1]

        features = {

            # ---------------------------------------
            # Store Information
            # ---------------------------------------

            "store": latest[STORE_COLUMN],

            # ---------------------------------------
            # Calendar Features
            # ---------------------------------------

            "dayofweek": future_date.dayofweek + 1,

            "promo": latest["promo"],

            "schoolholiday": latest["schoolholiday"],

            "customers": latest["customers"],

            "month": future_date.month,

            "week": int(future_date.isocalendar().week),

            "quarter": future_date.quarter,

            "is_weekend": int(
                future_date.dayofweek >= 5
            ),

            # ---------------------------------------
            # Lag Features
            # ---------------------------------------

            "lag_1": history[TARGET_COLUMN].iloc[-1],

            "lag_7": (
                history[TARGET_COLUMN].iloc[-7]
                if len(history) >= 7
                else history[TARGET_COLUMN].iloc[-1]
            ),

            # ---------------------------------------
            # Rolling Features
            # ---------------------------------------

            "rolling_mean_7": (
                history[TARGET_COLUMN]
                .tail(7)
                .mean()
            ),

            "rolling_mean_30": (
                history[TARGET_COLUMN]
                .tail(30)
                .mean()
            )

        }

        # ---------------------------------------
        # Create DataFrame
        # ---------------------------------------

        features_df = pd.DataFrame([features])

        # ---------------------------------------
        # Ensure all required columns exist
        # ---------------------------------------

        for column in FEATURE_COLUMNS:

            if column not in features_df.columns:

                features_df[column] = 0

        # ---------------------------------------
        # Force identical column order
        # ---------------------------------------

        features_df = features_df[FEATURE_COLUMNS]

        return features_df