import streamlit as st


class AnalysisPanel:
    """
    Reusable analysis panel for every module.

    Returns
    -------
    dict

    {
        "engine": str,
        "analysis_type": str,
        "generate": bool
    }
    """

    ANALYSIS_OPTIONS = {

        "forecast": [

            "Executive Summary",

            "Demand Analysis",

            "Risk Analysis",

            "Business Recommendations"

        ],

        "inventory": [

            "Inventory Assessment",

            "Risk Analysis",

            "Purchase Recommendation",

            "Optimization Suggestions"

        ],

        "dashboard": [

            "Executive Summary"

        ]

    }

    ENGINE_OPTIONS = [

        "AI Business Analyst",

        "Business Rules Engine"

    ]

    # --------------------------------------------------
    # Display Analysis Panel
    # --------------------------------------------------

    @classmethod
    def show(cls, module):

        if module not in cls.ANALYSIS_OPTIONS:

            raise ValueError(
                f"Unsupported module: {module}"
            )

        st.subheader("🧠 Analysis")

        col1, col2 = st.columns(2)

        with col1:

            engine = st.radio(

                "Analysis Engine",

                options=cls.ENGINE_OPTIONS,

                horizontal=True,

                key=f"{module}_analysis_engine"

            )

        with col2:

            analysis_type = st.selectbox(

                "Analysis Type",

                options=cls.ANALYSIS_OPTIONS[module],

                key=f"{module}_analysis_type"

            )

        generate = st.button(

            "🚀 Generate Analysis",

            use_container_width=True,

            type="primary",

            key=f"{module}_generate_analysis"

        )

        return {

            "engine": engine,

            "analysis_type": analysis_type,

            "generate": generate

        }