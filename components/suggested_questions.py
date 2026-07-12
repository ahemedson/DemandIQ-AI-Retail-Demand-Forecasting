import streamlit as st


class SuggestedQuestions:
    """
    Generates context-aware suggested questions
    for DemandIQ Copilot.
    """

    # --------------------------------------------------
    # Dataset Questions
    # --------------------------------------------------

    DATASET = [

        "Summarize the uploaded dataset.",

        "What are the key characteristics of this dataset?",

        "Identify any data quality issues.",

        "Explain the available features."

    ]

    # --------------------------------------------------
    # Forecast Questions
    # --------------------------------------------------

    FORECAST = [

        "Summarize the demand forecast.",

        "Explain the forecast accuracy.",

        "What business risks do you identify from the forecast?",

        "What actions should management take based on the forecast?"

    ]

    # --------------------------------------------------
    # Inventory Questions
    # --------------------------------------------------

    INVENTORY = [

        "Assess the inventory health.",

        "Should additional inventory be purchased?",

        "What is the current stockout risk?",

        "Suggest inventory optimization opportunities."

    ]

    # --------------------------------------------------
    # Get Suggestions
    # --------------------------------------------------

    @classmethod
    def get(cls):

        questions = []

        # Dataset uploaded

        if st.session_state.get("dataset") is not None:

            questions.extend(

                cls.DATASET

            )

        # Forecast generated

        if st.session_state.get("forecast_df") is not None:

            questions.extend(

                cls.FORECAST

            )

        # Inventory generated

        if st.session_state.get("inventory_summary") is not None:

            questions.extend(

                cls.INVENTORY

            )

        return questions


# --------------------------------------------------
# Display Suggested Questions
# --------------------------------------------------

def show_suggested_questions():
    """
    Displays suggested question buttons.

    Returns
    -------
    str | None

    Returns the selected question.
    """

    questions = SuggestedQuestions.get()

    if not questions:

        return None

    cols = st.columns(2)

    for index, question in enumerate(questions):

        with cols[index % 2]:

            if st.button(

                f"💬 {question}",

                use_container_width=True,

                key=f"suggested_{index}"

            ):

                return question

    return None