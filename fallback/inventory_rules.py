from datetime import datetime


class InventoryRules:
    """
    Business Rules Engine for inventory analysis.
    """

    def __init__(self, summary):

        self.summary = summary

    # --------------------------------------------------
    # Generate Analysis
    # --------------------------------------------------

    def generate(
        self,
        analysis_type="Inventory Assessment"
    ):

        generators = {

            "Inventory Assessment":
                self._assessment,

            "Risk Analysis":
                self._risk,

            "Purchase Recommendation":
                self._purchase,

            "Optimization Suggestions":
                self._optimization

        }

        report = generators.get(

            analysis_type,

            self._assessment

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
    # Assessment
    # --------------------------------------------------

    def _assessment(self):

        return f"""
# Inventory Assessment

Current Stock

**{self.summary['Current Stock']:,.0f}**

Safety Stock

**{self.summary['Safety Stock']:,.0f}**

Days of Inventory

**{self.summary['Days of Inventory']:.1f}**

Stockout Risk

**{self.summary['Stockout Risk']}**
"""

    # --------------------------------------------------
    # Risk
    # --------------------------------------------------

    def _risk(self):

        return f"""
# Risk Analysis

Current inventory risk is

**{self.summary['Stockout Risk']}**

Reorder Point

**{self.summary['Reorder Point']:,.0f}**

Average Daily Demand

**{self.summary['Average Daily Demand']:,.0f}**
"""

    # --------------------------------------------------
    # Purchase
    # --------------------------------------------------

    def _purchase(self):

        qty = self.summary["Recommended Purchase"]

        if qty <= 0:

            recommendation = (
                "No purchase is required."
            )

        else:

            recommendation = (

                f"Purchase approximately "

                f"**{qty:,.0f}** units."

            )

        return f"""
# Purchase Recommendation

{recommendation}
"""

    # --------------------------------------------------
    # Optimization
    # --------------------------------------------------

    def _optimization(self):

        return f"""
# Inventory Optimization

• Monitor inventory weekly.

• Maintain safety stock of
**{self.summary['Safety Stock']:,.0f}**

• Review reorder point regularly.

• Reduce excess stock during
low-demand periods.
"""