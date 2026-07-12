import pandas as pd

from reports.report_models import (
    KPI,
    ExecutiveAlert,
    ExecutiveScore,
    ReportChart,
    ReportSection,
    ReportTable
)


class ReportSections:
    """
    Builds every section of the Executive
    Intelligence Report.

    Every method returns a ReportSection.
    """

    # ==================================================
    # Helper Methods
    # ==================================================

    @staticmethod
    def _safe(value, default="-"):

        if value is None:
            return default

        if isinstance(value, float):

            if pd.isna(value):

                return default

        return value

    @staticmethod
    def _table_from_dataframe(
        title,
        dataframe,
        max_rows=20
    ):

        if dataframe is None or dataframe.empty:

            return None

        df = dataframe.head(max_rows).copy()

        return ReportTable(

            title=title,

            columns=list(df.columns),

            rows=df.values.tolist()

        )

    # ==================================================
    # Executive Summary
    # ==================================================

    @staticmethod
    def executive_summary(
        dataset,
        forecast_df,
        model_summary,
        inventory_summary,
        ai_reports
    ):

        rows = 0

        if dataset is not None:

            rows = len(dataset)

        forecast_days = 0

        if forecast_df is not None:

            forecast_days = len(forecast_df)

        best_model = "-"

        if model_summary:

            best_model = model_summary.get(

                "Best Model",

                "-"

            )

        stock_status = "-"

        if inventory_summary:

            stock_status = inventory_summary.get(

                "Stockout Risk",

                "-"

            )

        content = f"""

This report provides an executive overview of business performance,
forecasting intelligence and inventory planning.

The report was generated using the DemandIQ Analytics Platform.

Dataset Size : {rows:,} records

Forecast Horizon : {forecast_days} days

Best Forecast Model : {best_model}

Inventory Status : {stock_status}

The following sections provide detailed KPI analysis,
forecast evaluation, inventory intelligence,
business risks and AI recommendations.

"""

        kpis = [

            KPI(

                title="Dataset Rows",

                value=f"{rows:,}"

            ),

            KPI(

                title="Forecast Days",

                value=str(forecast_days)

            ),

            KPI(

                title="Forecast Model",

                value=best_model

            ),

            KPI(

                title="Inventory",

                value=stock_status

            )

        ]

        return ReportSection(

            title="Executive Summary",

            subtitle="High-level overview of the business intelligence report.",

            content=content,

            kpis=kpis

        )
        # ==================================================
    # Executive Scorecard
    # ==================================================

    @staticmethod
    def executive_scorecard(
        dataset,
        model_summary,
        inventory_summary
    ):

        # -------------------------------
        # Data Quality Score
        # -------------------------------

        if dataset is None:

            data_score = 0

        else:

            missing = int(dataset.isna().sum().sum())

            duplicates = int(dataset.duplicated().sum())

            penalty = missing + duplicates

            data_score = max(

                0,

                100 - penalty

            )

        # -------------------------------
        # Forecast Score
        # -------------------------------

        forecast_score = 80

        if model_summary:

            r2 = model_summary.get("R2")

            if r2 is not None:

                forecast_score = max(

                    0,

                    min(

                        100,

                        round(r2 * 100, 1)

                    )

                )

        # -------------------------------
        # Inventory Score
        # -------------------------------

        inventory_score = 80

        inventory_grade = "B"

        inventory_description = "Inventory levels are acceptable."

        if inventory_summary:

            risk = str(

                inventory_summary.get(

                    "Stockout Risk",

                    ""

                )

            ).lower()

            if "high" in risk:

                inventory_score = 40

                inventory_grade = "D"

                inventory_description = (

                    "High stockout risk detected."

                )

            elif "medium" in risk:

                inventory_score = 70

                inventory_grade = "B"

                inventory_description = (

                    "Inventory requires monitoring."

                )

            else:

                inventory_score = 95

                inventory_grade = "A"

                inventory_description = (

                    "Inventory health is excellent."

                )

        # -------------------------------
        # Overall Score
        # -------------------------------

        overall = round(

            (

                data_score +

                forecast_score +

                inventory_score

            ) / 3,

            1

        )

        def grade(score):

            if score >= 90:

                return "A"

            if score >= 80:

                return "B"

            if score >= 70:

                return "C"

            if score >= 60:

                return "D"

            return "F"

        scores = [

            ExecutiveScore(

                title="Data Quality",

                score=data_score,

                grade=grade(data_score),

                description="Dataset completeness and consistency."

            ),

            ExecutiveScore(

                title="Forecast Reliability",

                score=forecast_score,

                grade=grade(forecast_score),

                description="Forecast model performance."

            ),

            ExecutiveScore(

                title="Inventory Health",

                score=inventory_score,

                grade=inventory_grade,

                description=inventory_description

            ),

            ExecutiveScore(

                title="Overall Business Health",

                score=overall,

                grade=grade(overall),

                description="Combined executive score."

            )

        ]

        return ReportSection(

            title="Executive Scorecard",

            subtitle="Overall business performance assessment.",

            scores=scores

        )

    # ==================================================
    # Executive Alerts
    # ==================================================

    @staticmethod
    def executive_alerts(
        dataset,
        forecast_df,
        inventory_summary
    ):

        alerts = []

        # -------------------------------
        # Missing Values
        # -------------------------------

        if dataset is not None:

            missing = int(

                dataset.isna().sum().sum()

            )

            if missing > 0:

                alerts.append(

                    ExecutiveAlert(

                        level="Medium",

                        title="Missing Values",

                        description=(
                            f"The dataset contains {missing:,} missing values."
                        )

                    )

                )

        # -------------------------------
        # Inventory Risk
        # -------------------------------

        if inventory_summary:

            risk = inventory_summary.get(

                "Stockout Risk",

                "Unknown"

            )

            if str(risk).lower() == "high":

                alerts.append(

                    ExecutiveAlert(

                        level="High",

                        title="Stockout Risk",

                        description=(
                            "Inventory is expected to run out within the selected forecast horizon."
                        )

                    )

                )

        # -------------------------------
        # Forecast Horizon
        # -------------------------------

        if forecast_df is not None:

            if len(forecast_df) >= 90:

                alerts.append(

                    ExecutiveAlert(

                        level="Low",

                        title="Long Forecast Horizon",

                        description=(
                            "Forecast extends over a long period. Monitor predictions periodically."
                        )

                    )

                )

        if not alerts:

            alerts.append(

                ExecutiveAlert(

                    level="Low",

                    title="No Critical Risks",

                    description=(
                        "No significant operational issues were detected."
                    )

                )

            )

        return ReportSection(

            title="Executive Alerts",

            subtitle="Business risks requiring management attention.",

            alerts=alerts

        )
        # ==================================================
    # Dataset Overview
    # ==================================================

    @staticmethod
    def dataset_overview(
        dataset
    ):

        if dataset is None:

            return ReportSection(

                title="Dataset Overview",

                subtitle="Dataset Summary",

                content="No dataset has been uploaded."

            )

        rows = len(dataset)

        columns = len(dataset.columns)

        memory = dataset.memory_usage(

            deep=True

        ).sum() / (1024 * 1024)

        numeric_columns = len(

            dataset.select_dtypes(

                include="number"

            ).columns

        )

        categorical_columns = columns - numeric_columns

        kpis = [

            KPI(

                "Rows",

                f"{rows:,}"

            ),

            KPI(

                "Columns",

                columns

            ),

            KPI(

                "Numeric Columns",

                numeric_columns

            ),

            KPI(

                "Memory Usage",

                f"{memory:.2f} MB"

            )

        ]

        overview = ReportTable(

            title="Dataset Information",

            columns=[

                "Metric",

                "Value"

            ],

            rows=[

                [

                    "Rows",

                    f"{rows:,}"

                ],

                [

                    "Columns",

                    columns

                ],

                [

                    "Numeric Columns",

                    numeric_columns

                ],

                [

                    "Categorical Columns",

                    categorical_columns

                ],

                [

                    "Memory Usage",

                    f"{memory:.2f} MB"

                ]

            ]

        )

        preview = ReportTable(

            title="Dataset Preview",

            columns=list(dataset.columns),

            rows=dataset.head(10).values.tolist()

        )

        return ReportSection(

            title="Dataset Overview",

            subtitle="General information about the uploaded dataset.",

            content=(

                "This section summarizes the uploaded retail dataset "
                "and provides a preview of the available records."

            ),

            kpis=kpis,

            tables=[

                overview,

                preview

            ]

        )

    # ==================================================
    # Data Quality Assessment
    # ==================================================

    @staticmethod
    def data_quality(
        dataset
    ):

        if dataset is None:

            return ReportSection(

                title="Data Quality Assessment",

                subtitle="Dataset Validation",

                content="No dataset available."

            )

        missing = dataset.isna().sum()

        duplicates = int(

            dataset.duplicated().sum()

        )

        rows = []

        for column in dataset.columns:

            rows.append(

                [

                    column,

                    dataset[column].dtype,

                    int(missing[column]),

                    round(

                        (

                            missing[column]

                            /

                            len(dataset)

                        )

                        * 100,

                        2

                    )

                ]

            )

        quality_table = ReportTable(

            title="Column Quality Summary",

            columns=[

                "Column",

                "Data Type",

                "Missing",

                "Missing %"

            ],

            rows=rows

        )

        kpis = [

            KPI(

                "Duplicate Rows",

                duplicates

            ),

            KPI(

                "Missing Values",

                int(missing.sum())

            ),

            KPI(

                "Complete Columns",

                int(

                    (missing == 0).sum()

                )

            ),

            KPI(

                "Columns",

                len(dataset.columns)

            )

        ]

        content = (

            "The uploaded dataset was assessed for completeness, "
            "duplicate records and missing values. The table below "
            "summarizes the quality of each column."

        )

        return ReportSection(

            title="Data Quality Assessment",

            subtitle="Validation of the uploaded dataset.",

            content=content,

            kpis=kpis,

            tables=[

                quality_table

            ]

        )
        # ==================================================
    # Business Performance
    # ==================================================

    @staticmethod
    def business_performance(
        forecast_df,
        model_summary,
        inventory_summary
    ):

        if forecast_df is None:

            return ReportSection(

                title="Business Performance",

                subtitle="Business Performance Overview",

                content="No forecast has been generated."

            )

        # ------------------------------------------
        # Forecast KPIs
        # ------------------------------------------

        total_forecast = 0
        average_forecast = 0
        peak_forecast = 0
        minimum_forecast = 0

        if "Forecast" in forecast_df.columns:

            total_forecast = forecast_df["Forecast"].sum()

            average_forecast = forecast_df["Forecast"].mean()

            peak_forecast = forecast_df["Forecast"].max()

            minimum_forecast = forecast_df["Forecast"].min()

        best_model = "-"

        if model_summary:

            best_model = model_summary.get(

                "Best Model",

                "-"

            )

        stock_risk = "-"

        if inventory_summary:

            stock_risk = inventory_summary.get(

                "Stockout Risk",

                "-"

            )

        kpis = [

            KPI(

                "Total Forecast",

                f"{total_forecast:,.0f}"

            ),

            KPI(

                "Average Forecast",

                f"{average_forecast:,.2f}"

            ),

            KPI(

                "Peak Forecast",

                f"{peak_forecast:,.2f}"

            ),

            KPI(

                "Forecast Model",

                best_model

            )

        ]

        performance_table = ReportTable(

            title="Business Performance Summary",

            columns=[

                "Metric",

                "Value"

            ],

            rows=[

                [

                    "Forecast Horizon",

                    len(forecast_df)

                ],

                [

                    "Total Forecast",

                    f"{total_forecast:,.0f}"

                ],

                [

                    "Average Forecast",

                    f"{average_forecast:,.2f}"

                ],

                [

                    "Maximum Forecast",

                    f"{peak_forecast:,.2f}"

                ],

                [

                    "Minimum Forecast",

                    f"{minimum_forecast:,.2f}"

                ],

                [

                    "Best Forecast Model",

                    best_model

                ],

                [

                    "Inventory Risk",

                    stock_risk

                ]

            ]

        )

        content = (

            "Business performance is evaluated using the generated "
            "forecast, selected forecasting model and inventory "
            "assessment. These metrics provide an overview of "
            "expected operational performance during the selected "
            "forecast horizon."

        )

        return ReportSection(

            title="Business Performance",

            subtitle="Overall business performance indicators.",

            content=content,

            kpis=kpis,

            tables=[

                performance_table

            ]

        )
        # ==================================================
    # Forecast Analysis
    # ==================================================

    @staticmethod
    def forecast_analysis(
        forecast_df,
        model_summary
    ):

        if forecast_df is None:

            return ReportSection(

                title="Demand Forecast Analysis",

                subtitle="Demand Forecast",

                content="No demand forecast has been generated."

            )

        # ------------------------------------------
        # Forecast Statistics
        # ------------------------------------------

        total = 0
        average = 0
        maximum = 0
        minimum = 0

        if "Forecast" in forecast_df.columns:

            total = forecast_df["Forecast"].sum()

            average = forecast_df["Forecast"].mean()

            maximum = forecast_df["Forecast"].max()

            minimum = forecast_df["Forecast"].min()

        model_name = "-"

        if model_summary:

            model_name = model_summary.get(

                "Best Model",

                "-"

            )

        # ------------------------------------------
        # KPI Cards
        # ------------------------------------------

        kpis = [

            KPI(

                "Forecast Days",

                len(forecast_df)

            ),

            KPI(

                "Total Forecast",

                f"{total:,.0f}"

            ),

            KPI(

                "Average Forecast",

                f"{average:,.2f}"

            ),

            KPI(

                "Best Model",

                model_name

            )

        ]

        # ------------------------------------------
        # Forecast Table
        # ------------------------------------------

        forecast_table = ReportTable(

            title="Forecast Results",

            columns=list(forecast_df.columns),

            rows=forecast_df.round(2).values.tolist()

        )

        # ------------------------------------------
        # Forecast Chart
        # ------------------------------------------

        forecast_chart = ReportChart(

            title="Demand Forecast"

        )

        # ------------------------------------------
        # Section Content
        # ------------------------------------------

        content = (

            "The forecasting engine predicts future product demand "
            "using the selected machine learning model. "
            "The following results summarize the expected demand "
            "over the chosen forecasting horizon."

        )

        return ReportSection(

            title="Demand Forecast Analysis",

            subtitle="Forecasted demand trends and business outlook.",

            content=content,

            kpis=kpis,

            tables=[

                forecast_table

            ],

            charts=[

                forecast_chart

            ]

        )
        # ==================================================
    # Model Evaluation
    # ==================================================

    @staticmethod
    def model_evaluation(
        model_summary
    ):

        if not model_summary:

            return ReportSection(

                title="Forecast Model Evaluation",

                subtitle="Model Performance",

                content="Model evaluation metrics are not available."

            )

        # ------------------------------------------
        # KPIs
        # ------------------------------------------

        kpis = [

            KPI(

                "Best Model",

                model_summary.get(

                    "Best Model",

                    "-"

                )

            )

        ]

        metric_rows = []

        excluded = {

            "Best Model"

        }

        for key, value in model_summary.items():

            if key in excluded:

                continue

            if isinstance(

                value,

                float

            ):

                value = round(

                    value,

                    4

                )

            metric_rows.append(

                [

                    key,

                    value

                ]

            )

        metrics_table = ReportTable(

            title="Model Performance Metrics",

            columns=[

                "Metric",

                "Value"

            ],

            rows=metric_rows

        )

        content = (

            "The forecasting models were trained and evaluated "
            "using historical sales data. The model with the "
            "best predictive performance was selected "
            "automatically. The following metrics summarize "
            "its performance."

        )

        return ReportSection(

            title="Forecast Model Evaluation",

            subtitle="Machine learning model performance summary.",

            content=content,

            kpis=kpis,

            tables=[

                metrics_table

            ]

        )
        # ==================================================
    # Inventory Intelligence
    # ==================================================

    @staticmethod
    def inventory_intelligence(
        inventory_summary
    ):

        if inventory_summary is None:

            return ReportSection(

                title="Inventory Intelligence",

                subtitle="Inventory Analysis",

                content="Inventory analysis has not been generated."

            )

        # ------------------------------------------
        # KPI Cards
        # ------------------------------------------

        kpis = []

        table_rows = []

        priority_keys = [

            "Current Stock",

            "Forecast Demand",

            "Recommended Stock",

            "Safety Stock",

            "Reorder Point",

            "Lead Time Demand",

            "Stockout Risk"

        ]

        for key in priority_keys:

            if key in inventory_summary:

                value = inventory_summary[key]

                kpis.append(

                    KPI(

                        title=key,

                        value=str(value)

                    )

                )

                table_rows.append(

                    [

                        key,

                        value

                    ]

                )

        # ------------------------------------------
        # Include Remaining Values
        # ------------------------------------------

        for key, value in inventory_summary.items():

            if key not in priority_keys:

                table_rows.append(

                    [

                        key,

                        value

                    ]

                )

        # ------------------------------------------
        # Inventory Summary Table
        # ------------------------------------------

        inventory_table = ReportTable(

            title="Inventory Planning Summary",

            columns=[

                "Metric",

                "Value"

            ],

            rows=table_rows

        )

        # ------------------------------------------
        # Inventory Projection Chart
        # ------------------------------------------

        inventory_chart = ReportChart(

            title="Inventory Projection"

        )

        # ------------------------------------------
        # Description
        # ------------------------------------------

        content = (

            "Inventory planning is based on the generated demand "
            "forecast together with the selected lead time and "
            "service level. The following results summarize the "
            "recommended inventory strategy and stock availability."

        )

        return ReportSection(

            title="Inventory Intelligence",

            subtitle="Inventory planning and stock optimization.",

            content=content,

            kpis=kpis,

            tables=[

                inventory_table

            ],

            charts=[

                inventory_chart

            ]

        )
        # ==================================================
    # Business Risks
    # ==================================================

    @staticmethod
    def business_risks(
        forecast_df,
        inventory_summary
    ):

        risks = []

        # ------------------------------------------
        # Forecast Risk
        # ------------------------------------------

        if forecast_df is not None:

            if "Forecast" in forecast_df.columns:

                demand_cv = (

                    forecast_df["Forecast"].std()

                    /

                    max(

                        forecast_df["Forecast"].mean(),

                        1

                    )

                )

                if demand_cv > 0.50:

                    risks.append(

                        ExecutiveAlert(

                            level="High",

                            title="Demand Volatility",

                            description=(
                                "Forecast demand shows high variability. "
                                "Inventory planning should be monitored "
                                "closely to avoid stockouts or excess stock."
                            )

                        )

                    )

                elif demand_cv > 0.25:

                    risks.append(

                        ExecutiveAlert(

                            level="Medium",

                            title="Moderate Demand Variation",

                            description=(
                                "Forecast demand varies moderately. "
                                "Periodic review of inventory levels "
                                "is recommended."
                            )

                        )

                    )

        # ------------------------------------------
        # Inventory Risk
        # ------------------------------------------

        if inventory_summary:

            risk = str(

                inventory_summary.get(

                    "Stockout Risk",

                    ""

                )

            ).lower()

            if "high" in risk:

                risks.append(

                    ExecutiveAlert(

                        level="High",

                        title="High Stockout Risk",

                        description=(
                            "Current inventory may not satisfy "
                            "forecast demand. Immediate replenishment "
                            "is recommended."
                        )

                    )

                )

            elif "medium" in risk:

                risks.append(

                    ExecutiveAlert(

                        level="Medium",

                        title="Potential Stockout",

                        description=(
                            "Inventory should be monitored carefully "
                            "during the forecast period."
                        )

                    )

                )

        # ------------------------------------------
        # Default
        # ------------------------------------------

        if not risks:

            risks.append(

                ExecutiveAlert(

                    level="Low",

                    title="Business Risk",

                    description=(
                        "No significant operational risks were "
                        "identified based on the current analysis."
                    )

                )

            )

        content = (

            "Business risks are identified using forecast behaviour "
            "and inventory planning metrics. These alerts highlight "
            "areas that may require management attention."

        )

        return ReportSection(

            title="Business Risk Assessment",

            subtitle="Operational risks identified from demand forecasting and inventory analysis.",

            content=content,

            alerts=risks

        )
        # ==================================================
    # AI Recommendations
    # ==================================================

    @staticmethod
    def ai_recommendations(
        ai_reports
    ):

        if not ai_reports:

            return ReportSection(

                title="AI Recommendations",

                subtitle="AI Business Insights",

                content=(
                    "No AI-generated recommendations are available."
                )

            )

        content_parts = []

        # ------------------------------------------
        # Forecast Analysis
        # ------------------------------------------

        forecast_report = ai_reports.get(

            "forecast"

        )

        if forecast_report:

            title = forecast_report.get(

                "title",

                "Forecast Analysis"

            )

            report_content = forecast_report.get(

                "content",

                ""

            )

            content_parts.append(

                f"<b>{title}</b><br/><br/>{report_content}"

            )

        # ------------------------------------------
        # Inventory Analysis
        # ------------------------------------------

        inventory_report = ai_reports.get(

            "inventory"

        )

        if inventory_report:

            title = inventory_report.get(

                "title",

                "Inventory Analysis"

            )

            report_content = inventory_report.get(

                "content",

                ""

            )

            if content_parts:

                content_parts.append("<br/><br/>")

            content_parts.append(

                f"<b>{title}</b><br/><br/>{report_content}"

            )

        # ------------------------------------------
        # No Reports
        # ------------------------------------------

        if not content_parts:

            content = (

                "Business analysis has not yet been generated. "
                "Generate AI insights from the Forecasting and "
                "Inventory Intelligence modules to include "
                "recommendations in this report."

            )

        else:

            content = "".join(

                content_parts

            )

        return ReportSection(

            title="AI Recommendations",

            subtitle="Business recommendations generated using AI.",

            content=content

        )