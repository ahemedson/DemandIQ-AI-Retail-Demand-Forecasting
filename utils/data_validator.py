import pandas as pd


class DataValidator:
    """
    Validates and standardizes the dataset before
    it is used anywhere in the application.
    """

    REQUIRED_COLUMNS = [
        "date",
        "sales"
    ]

    def __init__(self, df):

        self.df = df.copy()

    # --------------------------------------------------
    # Standardize Column Names
    # --------------------------------------------------

    def standardize_columns(self):

        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

    # --------------------------------------------------
    # Validate Required Columns
    # --------------------------------------------------

    def validate_columns(self):

        missing = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in self.df.columns
        ]

        if missing:

            raise ValueError(
                f"Missing required columns: {missing}"
            )

    # --------------------------------------------------
    # Standardize Data Types
    # --------------------------------------------------

    def standardize_dtypes(self):

        self.df["date"] = pd.to_datetime(
            self.df["date"],
            errors="coerce"
        )

        self.df["store"] = (
            self.df["store"]
            .fillna(0)
            .astype(int)
        )

        self.df["sales"] = (
            self.df["sales"]
            .fillna(0)
            .astype(float)
        )

        self.df["customers"] = (
            self.df["customers"]
            .fillna(0)
            .astype(int)
        )

        self.df["promo"] = (
            self.df["promo"]
            .fillna(0)
            .astype(int)
        )

        self.df["schoolholiday"] = (
            self.df["schoolholiday"]
            .fillna(0)
            .astype(int)
        )

        self.df["dayofweek"] = (
            self.df["dayofweek"]
            .fillna(0)
            .astype(int)
        )

        self.df["stateholiday"] = (
            self.df["stateholiday"]
            .fillna("0")
            .astype(str)
        )

    # --------------------------------------------------
    # Validate Missing Dates
    # --------------------------------------------------

    def validate_dates(self):

        if self.df["date"].isnull().any():

            raise ValueError(
                "Invalid dates found in the dataset."
            )

    # --------------------------------------------------
    # Run Validation
    # --------------------------------------------------

    def validate(self):

        self.standardize_columns()

        self.validate_columns()

        self.standardize_dtypes()

        self.validate_dates()

        return self.df