import pandas as pd
import plotly.express as px


class Charts:

    def __init__(self, df):
        self.df = df.copy()

    # --------------------------------------------------
    # Daily Sales Trend
    # --------------------------------------------------

    def daily_sales_trend(self):

        daily = (
            self.df.groupby("date", as_index=False)["sales"]
            .sum()
            .sort_values("date")
        )

        fig = px.line(
            daily,
            x="date",
            y="sales",
            title="Daily Sales Trend",
            markers=False
        )

        fig.update_layout(
            template="plotly_white",
            height=450,
            hovermode="x unified",
            xaxis_title="Date",
            yaxis_title="Sales"
        )

        return fig

    # --------------------------------------------------
    # Monthly Sales Trend
    # --------------------------------------------------

    def monthly_sales_trend(self):

        monthly = self.df.copy()

        monthly["month"] = (
            monthly["date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly = (
            monthly.groupby("month", as_index=False)["sales"]
            .sum()
        )

        fig = px.line(
            monthly,
            x="month",
            y="sales",
            markers=True,
            title="Monthly Sales Trend"
        )

        fig.update_layout(
            template="plotly_white",
            height=450,
            hovermode="x unified",
            xaxis_title="Month",
            yaxis_title="Sales"
        )

        return fig

    # --------------------------------------------------
    # Yearly Sales Trend
    # --------------------------------------------------

    def yearly_sales_trend(self):

        yearly = self.df.copy()

        yearly["year"] = yearly["date"].dt.year

        yearly = (
            yearly.groupby("year", as_index=False)["sales"]
            .sum()
        )

        fig = px.bar(
            yearly,
            x="year",
            y="sales",
            title="Yearly Sales Trend"
        )

        fig.update_layout(
            template="plotly_white",
            height=400,
            xaxis_title="Year",
            yaxis_title="Sales"
        )

        return fig

    # --------------------------------------------------
    # Sales by Store
    # --------------------------------------------------

    def sales_by_store(self):

        stores = (
            self.df.groupby("store", as_index=False)["sales"]
            .sum()
            .sort_values("sales", ascending=False)
        )

        fig = px.bar(
            stores,
            x="store",
            y="sales",
            title="Sales by Store"
        )

        fig.update_layout(
            template="plotly_white",
            height=400,
            xaxis_title="Store",
            yaxis_title="Sales"
        )

        return fig

    # --------------------------------------------------
    # Sales by Day
    # --------------------------------------------------

    def sales_by_day(self):

        days = (
            self.df.groupby("dayofweek", as_index=False)["sales"]
            .sum()
            .sort_values("dayofweek")
        )

        day_map = {
            1: "Mon",
            2: "Tue",
            3: "Wed",
            4: "Thu",
            5: "Fri",
            6: "Sat",
            7: "Sun"
        }

        days["dayofweek"] = days["dayofweek"].map(day_map)

        fig = px.bar(
            days,
            x="dayofweek",
            y="sales",
            title="Sales by Day of Week"
        )

        fig.update_layout(
            template="plotly_white",
            height=400,
            xaxis_title="Day",
            yaxis_title="Sales"
        )

        return fig

    # --------------------------------------------------
    # Promotion Impact
    # --------------------------------------------------

    def promotion_impact(self):

        promo = (
            self.df.groupby("promo", as_index=False)
            .agg(
                Average_Sales=("sales", "mean"),
                Average_Customers=("customers", "mean")
            )
        )

        promo["promo"] = promo["promo"].replace({
            0: "No Promotion",
            1: "Promotion"
        })

        fig = px.bar(
            promo,
            x="promo",
            y="Average_Sales",
            color="promo",
            title="Promotion Impact on Average Sales"
        )

        fig.update_layout(
            template="plotly_white",
            height=400,
            showlegend=False,
            xaxis_title="Promotion",
            yaxis_title="Average Sales"
        )

        return fig

    # --------------------------------------------------
    # Sales Distribution
    # --------------------------------------------------

    def sales_distribution(self):

        fig = px.histogram(
            self.df,
            x="sales",
            nbins=50,
            title="Sales Distribution"
        )

        fig.update_layout(
            template="plotly_white",
            height=400,
            xaxis_title="Sales",
            yaxis_title="Frequency"
        )

        return fig

    # --------------------------------------------------
    # Top Stores
    # --------------------------------------------------

    def top_stores(self):

        top = (
            self.df.groupby("store", as_index=False)["sales"]
            .sum()
            .sort_values("sales", ascending=False)
            .head(10)
        )

        fig = px.bar(
            top,
            x="store",
            y="sales",
            title="Top 10 Stores"
        )

        fig.update_layout(
            template="plotly_white",
            height=400
        )

        return fig

    # --------------------------------------------------
    # Bottom Stores
    # --------------------------------------------------

    def bottom_stores(self):

        bottom = (
            self.df.groupby("store", as_index=False)["sales"]
            .sum()
            .sort_values("sales")
            .head(10)
        )

        fig = px.bar(
            bottom,
            x="store",
            y="sales",
            title="Bottom 10 Stores"
        )

        fig.update_layout(
            template="plotly_white",
            height=400
        )

        return fig