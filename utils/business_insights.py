import pandas as pd


class BusinessInsights:

    def __init__(self, df):
        self.df = df.copy()

    def generate(self):

        insights = []

        # --------------------------------------------------
        # Promotion Impact
        # --------------------------------------------------

        if "promo" in self.df.columns:

            promo_sales = (
                self.df.groupby("promo")["sales"]
                .mean()
            )

            if len(promo_sales) == 2:

                improvement = (
                    (promo_sales[1] - promo_sales[0])
                    / promo_sales[0]
                ) * 100

                insights.append(
                    f"🎁 Promotions increase average sales by {improvement:.1f}%."
                )

        # --------------------------------------------------
        # Best Performing Day
        # --------------------------------------------------

        if "dayofweek" in self.df.columns:

            day_sales = (
                self.df.groupby("dayofweek")["sales"]
                .sum()
            )

            best_day = day_sales.idxmax()

            days = {
                1: "Monday",
                2: "Tuesday",
                3: "Wednesday",
                4: "Thursday",
                5: "Friday",
                6: "Saturday",
                7: "Sunday"
            }

            insights.append(
                f"📅 {days[best_day]} generates the highest total sales."
            )

        # --------------------------------------------------
        # Best Store
        # --------------------------------------------------

        if "store" in self.df.columns:

            stores = (
                self.df.groupby("store")["sales"]
                .sum()
            )

            best_store = stores.idxmax()

            insights.append(
                f"🏪 Store {best_store} is the highest-performing store."
            )

        # --------------------------------------------------
        # Best Month
        # --------------------------------------------------

        monthly = self.df.copy()

        monthly["month"] = (
            monthly["date"]
            .dt.month_name()
        )

        month_sales = (
            monthly.groupby("month")["sales"]
            .sum()
        )

        best_month = month_sales.idxmax()

        insights.append(
            f"📈 {best_month} records the highest monthly sales."
        )

        # --------------------------------------------------
        # Customer Insight
        # --------------------------------------------------

        if "customers" in self.df.columns:

            avg_customers = (
                self.df["customers"]
                .mean()
            )

            insights.append(
                f"👥 Average daily customer count is {avg_customers:,.0f}."
            )

        # --------------------------------------------------
        # Holiday Insight
        # --------------------------------------------------

        if "stateholiday" in self.df.columns:

            holidays = (
                self.df[self.df["stateholiday"] != "0"]
            )

            if len(holidays) > 0:

                avg = holidays["sales"].mean()

                insights.append(
                    f"🎄 Average sales during state holidays are {avg:,.0f}."
                )

        return insights