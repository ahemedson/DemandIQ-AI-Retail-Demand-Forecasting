import pandas as pd


class DataLoader:

    def __init__(self):
        self.df = None

    def load_data(self, uploaded_file):
        """
        Load CSV file into a pandas DataFrame.
        """

        self.df = pd.read_csv(uploaded_file)

        return self.df

    def get_dataset_summary(self):
        """
        Returns basic dataset information.
        """

        return {
            "Rows": self.df.shape[0],
            "Columns": self.df.shape[1],
            "Memory Usage (MB)": round(
                self.df.memory_usage(deep=True).sum() / (1024 ** 2),
                2
            )
        }

    def get_column_details(self):
        """
        Returns information about each column.
        """

        return pd.DataFrame({
            "Column": self.df.columns,
            "Data Type": self.df.dtypes.astype(str),
            "Missing Values": self.df.isnull().sum(),
            "Unique Values": self.df.nunique()
        })

    def get_missing_values(self):
        """
        Returns missing value statistics.
        """

        missing = pd.DataFrame({
            "Column": self.df.columns,
            "Missing Values": self.df.isnull().sum()
        })

        missing["Missing %"] = round(
            (missing["Missing Values"] / len(self.df)) * 100,
            2
        )

        return missing

    def get_duplicate_count(self):
        """
        Returns duplicate row count.
        """

        return self.df.duplicated().sum()

    def get_preview(self):
        """
        Returns first 10 rows.
        """

        return self.df.head(10)

    def get_statistics(self):
        """
        Returns statistical summary.
        """

        return self.df.describe(include="all")