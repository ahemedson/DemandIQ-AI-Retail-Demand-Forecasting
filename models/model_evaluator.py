import pandas as pd


class ModelEvaluator:
    """
    Collects and compares the performance
    of multiple forecasting models.
    """

    def __init__(self):

        self.results = []

    # --------------------------------------------------
    # Add Model Result
    # --------------------------------------------------

    def add_result(self, result):
        """
        Store a model's evaluation result.
        """

        self.results.append(result)

    # --------------------------------------------------
    # Get Comparison Table
    # --------------------------------------------------

    def get_results(self):
        """
        Return all model results sorted by RMSE.
        """

        if not self.results:
            return pd.DataFrame()

        df = pd.DataFrame(self.results)

        # Columns useful for comparison
        comparison = df[
            [
                "Model",
                "MAE",
                "RMSE",
                "R2"
            ]
        ]

        comparison = comparison.sort_values(
            by="RMSE",
            ascending=True
        )

        comparison.reset_index(
            drop=True,
            inplace=True
        )

        return comparison

    # --------------------------------------------------
    # Full Results
    # --------------------------------------------------

    def get_full_results(self):
        """
        Return complete model results,
        including predictions and model objects.
        """

        return self.results