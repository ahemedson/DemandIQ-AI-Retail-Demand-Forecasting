from datetime import datetime
import pandas as pd


class Formatter:
    """
    Centralized formatting utilities used across DemandIQ.
    """

    # --------------------------------------------------
    # Numbers
    # --------------------------------------------------

    @staticmethod
    def number(value, decimals=0):

        if pd.isna(value):
            return "-"

        return f"{value:,.{decimals}f}"

    # --------------------------------------------------
    # Sales / Revenue
    # --------------------------------------------------

    @staticmethod
    def sales(value):

        return Formatter.number(value)

    # --------------------------------------------------
    # Currency
    # --------------------------------------------------

    @staticmethod
    def currency(value, symbol="$"):

        if pd.isna(value):
            return "-"

        return f"{symbol}{value:,.2f}"

    # --------------------------------------------------
    # Percentage
    # --------------------------------------------------

    @staticmethod
    def percent(value, decimals=2):

        if pd.isna(value):
            return "-"

        return f"{value:.{decimals}f}%"

    # --------------------------------------------------
    # Date
    # --------------------------------------------------

    @staticmethod
    def date(value, fmt="%d %b %Y"):

        if pd.isna(value):
            return "-"

        if isinstance(value, str):
            value = pd.to_datetime(value)

        return value.strftime(fmt)

    # --------------------------------------------------
    # Integer
    # --------------------------------------------------

    @staticmethod
    def integer(value):

        if pd.isna(value):
            return "-"

        return f"{int(value):,}"