from models.feature_engineering import FeatureEngineering

from config.settings import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    TEST_SIZE
)


class ForecastPipeline:
    """
    Prepares the validated dataset for forecasting models.
    """

    def __init__(self, df):
        self.df = df.copy()

    def prepare_data(self):

        # ---------------------------------------
        # Feature Engineering
        # ---------------------------------------

        engineer = FeatureEngineering(self.df)

        data = engineer.create_features()

        # ---------------------------------------
        # Time-Based Train/Test Split
        # ---------------------------------------

        split_index = int(len(data) * (1 - TEST_SIZE))

        train = data.iloc[:split_index]

        test = data.iloc[split_index:]

        # ---------------------------------------
        # Features & Target
        # ---------------------------------------

        X_train = train[FEATURE_COLUMNS]

        y_train = train[TARGET_COLUMN]

        X_test = test[FEATURE_COLUMNS]

        y_test = test[TARGET_COLUMN]

        return (
            X_train,
            X_test,
            y_train,
            y_test
        )