from models.forecasting_engine import ForecastingEngine
from models.future_forecaster import FutureForecaster


class ForecastingService:
    """
    High-level service responsible for training models,
    selecting the best model, and generating future forecasts.
    """

    def __init__(self, df):

        self.df = df

        self.engine = ForecastingEngine(df)

        self.trained = False

        self.best_model_info = None

        self.best_model = None

    # --------------------------------------------------
    # Train Models
    # --------------------------------------------------

    def train(self):

        if self.trained:
            return

        self.engine.train_models()

        self.best_model_info = self.engine.best_model()

        model_name = self.best_model_info["Best Model"]

        self.best_model = self.engine.get_model(
            model_name
        )

        self.trained = True

    # --------------------------------------------------
    # Training Status
    # --------------------------------------------------

    def is_trained(self):

        return self.trained

    # --------------------------------------------------
    # Model Comparison
    # --------------------------------------------------

    def model_comparison(self):

        self.train()

        return self.engine.evaluation_results()

    # --------------------------------------------------
    # Best Model Summary
    # --------------------------------------------------

    def best_model_summary(self):

        self.train()

        return self.best_model_info

    # --------------------------------------------------
    # Best Trained Model
    # --------------------------------------------------

    def get_best_model(self):

        self.train()

        return self.best_model

    # --------------------------------------------------
    # Future Forecast
    # --------------------------------------------------

    def forecast(self, days=30):

        self.train()

        forecaster = FutureForecaster(

            self.best_model,

            self.df

        )

        return forecaster.forecast(days)

    # --------------------------------------------------
    # Predict Test Set
    # --------------------------------------------------

    def predict(self):

        self.train()

        return self.best_model.predict()