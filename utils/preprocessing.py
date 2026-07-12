import pandas as pd


class DataPreprocessor:

    def __init__(self, df):
        self.df = df.copy()

    def clean_column_names(self):
        """
        Convert column names to lowercase and replace spaces with underscores.
        """

        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        return self.df

    def convert_date_column(self):
        """
        Convert the 'date' column to datetime.
        """

        if "date" in self.df.columns:
            self.df["date"] = pd.to_datetime(
                self.df["date"],
                errors="coerce"
            )

        return self.df

    def remove_duplicates(self):
        """
        Remove duplicate rows.
        """

        before = len(self.df)

        self.df = self.df.drop_duplicates()

        removed = before - len(self.df)

        return removed

    def sort_by_date(self):
        """
        Sort dataset by date.
        """

        if "date" in self.df.columns:
            self.df = self.df.sort_values("date")

        return self.df

    def missing_value_report(self):
        """
        Return missing values.
        """

        return self.df.isnull().sum()

    def preprocess(self):
        """
        Complete preprocessing pipeline.
        """

        self.clean_column_names()

        self.convert_date_column()

        removed = self.remove_duplicates()

        self.sort_by_date()

        return self.df, removed