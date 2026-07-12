class ModelSelector:
    """
    Selects the best forecasting model based on
    evaluation metrics.
    """

    def __init__(self, results):

        self.results = results

    # --------------------------------------------------
    # Best Model
    # --------------------------------------------------

    def best_model(self):
        """
        Return the complete result dictionary of
        the best-performing model.
        """

        if not self.results:
            raise ValueError(
                "No model results available."
            )

        return min(
            self.results,
            key=lambda result: result["RMSE"]
        )

    # --------------------------------------------------
    # Best Model Name
    # --------------------------------------------------

    def best_model_name(self):

        return self.best_model()["Model"]

    # --------------------------------------------------
    # Best Model Object
    # --------------------------------------------------

    def best_model_object(self):

        return self.best_model()["Model Object"]

    # --------------------------------------------------
    # Best Predictions
    # --------------------------------------------------

    def best_predictions(self):

        return self.best_model()["Predictions"]

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(self):

        best = self.best_model()

        return {
            "Best Model": best["Model"],
            "MAE": best["MAE"],
            "RMSE": best["RMSE"],
            "R2": best["R2"]
        }