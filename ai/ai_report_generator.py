from utils.logger import Logger

from ai.llm_service import LLMService
from ai.prompt_builder import PromptBuilder
from ai.response_parser import ResponseParser

from fallback.forecast_rules import ForecastRules
from fallback.inventory_rules import InventoryRules


logger = Logger.get_logger()


class AIReportGenerator:
    """
    Central AI report generation service.

    Supports:
        • AI Business Analyst
        • Business Rules Engine

    Returns a standardized response object for every report.
    """

    # Shared LLM instance for the entire application
    _llm = LLMService()

    # --------------------------------------------------
    # Rule Engine Registry
    # --------------------------------------------------

    _RULE_ENGINES = {

        "forecast": ForecastRules,

        "inventory": InventoryRules

    }

    # --------------------------------------------------
    # Prompt Mapping
    # --------------------------------------------------

    _PROMPTS = {

        "forecast": {

            "Executive Summary": "executive",

            "Demand Analysis": "demand",

            "Risk Analysis": "risk",

            "Business Recommendations": "recommendation"

        },

        "inventory": {

            "Inventory Assessment": "assessment",

            "Risk Analysis": "risk",

            "Purchase Recommendation": "purchase",

            "Optimization Suggestions": "optimization"

        }

    }

    # --------------------------------------------------
    # Generate Report
    # --------------------------------------------------

    def generate(

        self,

        engine,

        module,

        analysis_type,

        variables,

        fallback_data

    ):

        if engine == "AI Business Analyst":

            return self._generate_ai(

                module,

                analysis_type,

                variables,

                fallback_data

            )

        return self._generate_rules(

            module,

            analysis_type,

            fallback_data

        )

    # --------------------------------------------------
    # AI Generation
    # --------------------------------------------------

    def _generate_ai(

        self,

        module,

        analysis_type,

        variables,

        fallback_data

    ):

        try:

            template = self._PROMPTS[module][analysis_type]

            prompt = PromptBuilder.build(

                module=module,

                template=template,

                variables=variables

            )

            response = self._llm.generate(

                prompt=prompt

            )

            parsed = ResponseParser.parse(

                response

            )

            if parsed["success"]:

                return {

                    **parsed,

                    "title": analysis_type

                }

            logger.warning(

                "AI response unsuccessful. "

                "Using Business Rules."

            )

        except Exception:

            logger.exception(

                "AI report generation failed."

            )

        return self._generate_rules(

            module,

            analysis_type,

            fallback_data

        )

    # --------------------------------------------------
    # Business Rules
    # --------------------------------------------------

    def _generate_rules(

        self,

        module,

        analysis_type,

        fallback_data

    ):

        if module not in self._RULE_ENGINES:

            raise ValueError(

                f"Unsupported module: {module}"

            )

        rule_engine = self._RULE_ENGINES[module]

        if module == "forecast":

            report = rule_engine(

                forecast_df=fallback_data["forecast"],

                model_summary=fallback_data["model_summary"]

            )

        elif module == "inventory":

            report = rule_engine(

                fallback_data["summary"]

            )

        else:

            raise ValueError(

                f"Unsupported module: {module}"

            )

        return report.generate(

            analysis_type

        )