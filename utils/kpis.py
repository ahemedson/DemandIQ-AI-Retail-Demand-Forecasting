class KPI:

    def __init__(self, df):
        self.df = df

    def get_kpis(self):

        total_sales = self.df["sales"].sum()

        total_stores = self.df["store"].nunique()

        total_customers = (
            self.df["customers"].sum()
            if "customers" in self.df.columns
            else 0
        )

        start_date = self.df["date"].min().date()

        end_date = self.df["date"].max().date()

        return {
            "Total Sales": f"₹ {total_sales:,.0f}",
            "Stores": total_stores,
            "Customers": f"{total_customers:,.0f}",
            "Date Range": f"{start_date} → {end_date}"
        }