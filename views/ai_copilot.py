import streamlit as st

from ai.conversation_manager import ConversationManager
from ai.copilot_service import CopilotService

from components.suggested_questions import show_suggested_questions
from components.chat_message import show_chat_history
from components.chat_input import show_chat_input


# --------------------------------------------------
# Session Initialization
# --------------------------------------------------

def initialize_session():

    ConversationManager.initialize()

    defaults = {

        "copilot_service": None

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# --------------------------------------------------
# DemandIQ Copilot
# --------------------------------------------------

def show():

    initialize_session()

    st.title("🤖 DemandIQ Copilot")

    st.caption(

        "Ask business questions about your retail data, forecasts and inventory."

    )

    # --------------------------------------------------
    # Dataset Check
    # --------------------------------------------------

    if st.session_state.dataset is None:

        st.info(

            "👈 Upload a retail dataset to start using DemandIQ Copilot."

        )

        return

    # --------------------------------------------------
    # Initialize Copilot
    # --------------------------------------------------

    if st.session_state.copilot_service is None:

        st.session_state.copilot_service = CopilotService()

    service = st.session_state.copilot_service

    # --------------------------------------------------
    # Welcome Card
    # --------------------------------------------------

    if not ConversationManager.has_messages():

        st.info(

            """
### 👋 Welcome to DemandIQ Copilot

I can help you understand your:

- 📊 Uploaded retail dataset
- 📈 Demand forecasts
- 📦 Inventory recommendations
- ⚠ Business risks
- 💡 Business opportunities

Select one of the suggested questions below or ask your own question.
            """

        )

    # --------------------------------------------------
    # Suggested Questions
    # --------------------------------------------------

    st.subheader("💡 Suggested Questions")

    question = show_suggested_questions()

    # --------------------------------------------------
    # Conversation
    # --------------------------------------------------

    st.subheader("💬 Conversation")

    show_chat_history()

    # --------------------------------------------------
    # Conversation Controls
    # --------------------------------------------------

    col1, col2 = st.columns([1, 4])

    with col1:

        if st.button(

            "🗑 Clear Chat",

            use_container_width=True

        ):

            ConversationManager.clear()

            st.rerun()

    # --------------------------------------------------
    # Suggested Question Selected
    # --------------------------------------------------

    if question:

        with st.spinner(

            "DemandIQ is thinking..."

        ):

            response = service.ask(question)

        if response["success"]:

            st.rerun()

        else:

            st.error(

                response.get(

                    "error",

                    response.get(

                        "content",

                        "Unable to generate response."

                    )

                )

            )

    # --------------------------------------------------
    # Chat Input
    # --------------------------------------------------

    user_question = show_chat_input()

    if user_question:

        with st.spinner(

            "DemandIQ is analyzing your business..."

        ):

            response = service.ask(user_question)

        if response["success"]:

            st.rerun()

        else:

            st.error(

                response.get(

                    "error",

                    response.get(

                        "content",

                        "Unable to generate response."

                    )

                )

            )

    # --------------------------------------------------
    # Footer
    # --------------------------------------------------

    st.divider()

    st.caption(

        "DemandIQ Copilot uses your uploaded dataset, "

        "forecast results, inventory analysis and "

        "conversation history to answer business questions."

    )