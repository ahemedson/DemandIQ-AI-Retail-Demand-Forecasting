import pandas as pd

from config.settings import (
    STORE_COLUMN,
    DATE_COLUMN,
    TARGET_COLUMN
)


class FeatureEngineering:
    """
    Creates machine learning features for demand forecasting.
    """

    def __init__(self, df):
        self.df = df.copy()

    def create_features(self):

        # ---------------------------------------
        # Sort Dataset
        # ---------------------------------------

        self.df = self.df.sort_values(
            [STORE_COLUMN, DATE_COLUMN]
        )

        # ---------------------------------------
        # Date Features
        # ---------------------------------------

        self.df["year"] = self.df[DATE_COLUMN].dt.year
        self.df["month"] = self.df[DATE_COLUMN].dt.month
        self.df["day"] = self.df[DATE_COLUMN].dt.day
        self.df["week"] = (
            self.df[DATE_COLUMN]
            .dt.isocalendar()
            .week
            .astype(int)
        )
        self.df["quarter"] = self.df[DATE_COLUMN].dt.quarter

        # ---------------------------------------
        # Weekend Feature
        # ---------------------------------------

        self.df["is_weekend"] = (
            self.df["dayofweek"] >= 6
        ).astype(int)

        # ---------------------------------------
        # Lag Features
        # ---------------------------------------

        self.df["lag_1"] = (
            self.df.groupby(STORE_COLUMN)[TARGET_COLUMN]
            .shift(1)
        )

        self.df["lag_7"] = (
            self.df.groupby(STORE_COLUMN)[TARGET_COLUMN]
            .shift(7)
        )

        # ---------------------------------------
        # Rolling Mean Features
        # ---------------------------------------

        self.df["rolling_mean_7"] = (
            self.df.groupby(STORE_COLUMN)[TARGET_COLUMN]
            .transform(
                lambda x: x.shift(1).rolling(7).mean()
            )
        )

        self.df["rolling_mean_30"] = (
            self.df.groupby(STORE_COLUMN)[TARGET_COLUMN]
            .transform(
                lambda x: x.shift(1).rolling(30).mean()
            )
        )

        # ---------------------------------------
        # Fill Only Engineered Features
        # ---------------------------------------

        engineered_columns = [
            "lag_1",
            "lag_7",
            "rolling_mean_7",
            "rolling_mean_30"
        ]

        self.df[engineered_columns] = (
            self.df[engineered_columns]
            .fillna(0)
        )

        return self.df