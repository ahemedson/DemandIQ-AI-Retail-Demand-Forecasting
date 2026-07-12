from datetime import datetime

import pandas as pd


class ForecastRules:
    """
    Business Rules Engine for forecast analysis.

    Used when:
    - User selects Business Rules Engine
    - AI is unavailable
    """

    def __init__(
        self,
        forecast_df: pd.DataFrame,
        model_summary: dict
    ):

        self.forecast = forecast_df

        self.model = model_summary

    # --------------------------------------------------
    # Generate Analysis
    # --------------------------------------------------

    def generate(
        self,
        analysis_type="Executive Summary"
    ):

        generators = {

            "Executive Summary":
                self._executive_summary,

            "Demand Analysis":
                self._demand_analysis,

            "Risk Analysis":
                self._risk_analysis,

            "Business Recommendations":
                self._recommendations

        }

        report = generators.get(

            analysis_type,

            self._executive_summary

        )()

        return {

            "success": True,

            "engine": "Business Rules",

            "title": analysis_type,

            "content": report,

            "metadata": {

                "generated_at":

                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                "rule_version": "2.0"

            }

        }

    # --------------------------------------------------
    # Executive Summary
    # --------------------------------------------------

    def _executive_summary(self):

        total = self.forecast["Forecast"].sum()

        avg = self.forecast["Forecast"].mean()

        peak = self.forecast["Forecast"].max()

        return f"""
# Executive Summary

- Forecast horizon: **{len(self.forecast)} days**
- Total expected sales: **{total:,.0f}**
- Average daily demand: **{avg:,.0f}**
- Peak forecasted demand: **{peak:,.0f}**
- Best forecasting model: **{self.model['Best Model']}**
"""

    # --------------------------------------------------
    # Demand Analysis
    # --------------------------------------------------

    def _demand_analysis(self):

        trend = (

            "increasing"

            if self.forecast["Forecast"].iloc[-1]
            >

            self.forecast["Forecast"].iloc[0]

            else "stable"

        )

        return f"""
# Demand Analysis

Demand appears **{trend}** across the selected forecast horizon.

Average predicted sales are
**{self.forecast['Forecast'].mean():,.0f}**
units per day.

Peak demand reaches
**{self.forecast['Forecast'].max():,.0f}**
units.
"""

    # --------------------------------------------------
    # Risk Analysis
    # --------------------------------------------------

    def _risk_analysis(self):

        rmse = self.model["RMSE"]

        risk = (

            "Low"

            if rmse < 1000

            else "Moderate"

            if rmse < 2500

            else "High"

        )

        return f"""
# Risk Analysis

Forecast Accuracy Risk

**{risk}**

RMSE:

**{rmse:,.2f}**

Model:

**{self.model['Best Model']}**
"""

    # --------------------------------------------------
    # Recommendations
    # --------------------------------------------------

    def _recommendations(self):

        avg = self.forecast["Forecast"].mean()

        return f"""
# Business Recommendations

- Maintain inventory for approximately **{avg:,.0f}** units/day.
- Monitor demand spikes during peak forecast periods.
- Review replenishment schedules weekly.
- Continue using **{self.model['Best Model']}** for demand forecasting.
"""