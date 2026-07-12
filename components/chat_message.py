import streamlit as st

from ai.conversation_manager import ConversationManager


def show_chat_history():
    """
    Display the complete Copilot conversation.
    """

    history = ConversationManager.history()

    if not history:

        st.info(

            "Start a conversation with DemandIQ Copilot."

        )

        return

    for message in history:

        role = message["role"]

        avatar = "🤖" if role == "assistant" else "👤"

        with st.chat_message(

            name=role,

            avatar=avatar

        ):

            st.markdown(

                message["content"]

            )

            if "timestamp" in message:

                st.caption(

                    message["timestamp"].strftime(

                        "%d %b %Y • %I:%M %p"

                    )

                )