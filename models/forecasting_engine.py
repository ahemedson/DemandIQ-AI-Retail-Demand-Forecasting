from utils.logger import Logger

from models.forecast_pipeline import ForecastPipeline

from models.baseline_model import BaselineModel
from models.random_forest_model import RandomForestModel
from models.xgboost_model import XGBoostModel

from models.model_evaluator import ModelEvaluator
from models.model_selector import ModelSelector


logger = Logger.get_logger()


class ForecastingEngine:
    """
    Coordinates the complete forecasting workflow.
    """

    def __init__(self, df):

        self.df = df

        self.pipeline = ForecastPipeline(df)

        self.models = {}

        self.evaluator = ModelEvaluator()

        self.selector = None

        self.is_trained = False

        # -----------------------------------------
        # Available Forecasting Models
        # -----------------------------------------

        self.available_models = {
            "Baseline": BaselineModel,
            "Random Forest": RandomForestModel,
            "XGBoost": XGBoostModel
        }

    # --------------------------------------------------
    # Train All Models
    # --------------------------------------------------

    def train_models(self):

        # Prevent unnecessary retraining
        if self.is_trained:
            return

        if not self.available_models:
            raise ValueError(
                "No forecasting models are configured."
            )

        logger.info(
            "Starting forecasting model training..."
        )

        X_train, X_test, y_train, y_test = (
            self.pipeline.prepare_data()
        )

        # Reset previous state
        self.models = {}
        self.evaluator = ModelEvaluator()
        self.selector = None

        for model_name, model_class in self.available_models.items():

            logger.info(
                f"Training {model_name}..."
            )

            model = model_class(
                X_train,
                X_test,
                y_train,
                y_test
            )

            model.train()

            self.models[model_name] = model

            self.evaluator.add_result(
                model.evaluate()
            )

            logger.info(
                f"{model_name} trained successfully."
            )

        self.is_trained = True

        logger.info(
            "Forecasting pipeline completed successfully."
        )

    # --------------------------------------------------
    # Model Comparison
    # --------------------------------------------------

    def evaluation_results(self):

        if not self.is_trained:
            self.train_models()

        return self.evaluator.get_results()

    # --------------------------------------------------
    # Best Model Summary
    # --------------------------------------------------

    def best_model(self):

        if not self.is_trained:
            self.train_models()

        self.selector = ModelSelector(
            self.evaluator.get_full_results()
        )

        return self.selector.summary()

    # --------------------------------------------------
    # Retrieve Trained Model
    # --------------------------------------------------

    def get_model(self, model_name):

        if not self.is_trained:
            self.train_models()

        model = self.models.get(model_name)

        if model is None:
            raise ValueError(
                f"Model '{model_name}' not found."
            )

        return model

    # --------------------------------------------------
    # Predict
    # --------------------------------------------------

    def predict(self, model_name=None):

        if not self.is_trained:
            self.train_models()

        if model_name is None:

            self.selector = ModelSelector(
                self.evaluator.get_full_results()
            )

            model = self.selector.best_model_object()

        else:

            model = self.get_model(model_name)

        logger.info(
            f"Generating predictions using {model.__class__.__name__}."
        )

        return model.predict()