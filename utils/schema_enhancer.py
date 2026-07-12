import pandas as pd


class SchemaEnhancer:
    """
    Enhances different retail datasets into the
    standardized DemandIQ schema.
    """

    def __init__(self, df):

        self.df = df.copy()

    # --------------------------------------------------
    # Create Missing Columns
    # --------------------------------------------------

    def create_missing_columns(self):

        defaults = {

            "store": 1,

            "customers": 0,

            "promo": 0,

            "stateholiday": "0",

            "schoolholiday": 0,

            "open": 1

        }

        for column, value in defaults.items():

            if column not in self.df.columns:

                self.df[column] = value

    # --------------------------------------------------
    # Create Day Of Week
    # --------------------------------------------------

    def create_dayofweek(self):

        if "dayofweek" not in self.df.columns:

            self.df["dayofweek"] = (
                self.df["date"]
                .dt.dayofweek + 1
            )

    # --------------------------------------------------
    # Sort Dataset
    # --------------------------------------------------

    def sort_dataset(self):

        if "store" in self.df.columns:

            self.df = self.df.sort_values(
                ["store", "date"]
            )

        else:

            self.df = self.df.sort_values(
                "date"
            )

    # --------------------------------------------------
    # Reset Index
    # --------------------------------------------------

    def reset_index(self):

        self.df.reset_index(
            drop=True,
            inplace=True
        )

    # --------------------------------------------------
    # Run Enhancement
    # --------------------------------------------------

    def enhance(self):

        self.create_missing_columns()

        self.create_dayofweek()

        self.sort_dataset()

        self.reset_index()

        return self.df