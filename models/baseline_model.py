import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


class BaselineModel:
    """
    Baseline forecasting model using the previous day's sales.
    """

    def __init__(
        self,
        X_train,
        X_test,
        y_train,
        y_test
    ):

        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

        self.predictions = None

    # -------------------------------------------------
    # Train
    # -------------------------------------------------

    def train(self):
        """
        Baseline model requires no training.
        """
        pass

    # -------------------------------------------------
    # Predict
    # -------------------------------------------------

    def predict(self, X=None):

        if X is None:
            X = self.X_test

        self.predictions = X["lag_1"].values

        return self.predictions

    # -------------------------------------------------
    # Evaluate
    # -------------------------------------------------

    def evaluate(self):

        if self.predictions is None:
            self.predict()

        mae = mean_absolute_error(
            self.y_test,
            self.predictions
        )

        rmse = np.sqrt(
            mean_squared_error(
                self.y_test,
                self.predictions
            )
        )

        r2 = r2_score(
            self.y_test,
            self.predictions
        )

        return {
            "Model": "Random Forest",
            "MAE": float(round(mae, 2)),
            "RMSE": float(round(rmse, 2)),
            "R2": float(round(r2, 4)),
            "Predictions": self.predictions,
            "Model Object": None
        }