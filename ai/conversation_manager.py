from datetime import datetime

import streamlit as st


class ConversationManager:
    """
    Manages the AI Business Copilot conversation.
    """

    SESSION_KEY = "copilot_history"

    MAX_HISTORY = 20

    # --------------------------------------------------
    # Initialize
    # --------------------------------------------------

    @classmethod
    def initialize(cls):

        if cls.SESSION_KEY not in st.session_state:

            st.session_state[cls.SESSION_KEY] = []

    # --------------------------------------------------
    # Internal Append
    # --------------------------------------------------

    @classmethod
    def _append(cls, role, content):

        cls.initialize()

        history = st.session_state[cls.SESSION_KEY]

        history.append({

            "role": role,

            "content": content,

            "timestamp": datetime.now()

        })

        if len(history) > cls.MAX_HISTORY:

            history[:] = history[-cls.MAX_HISTORY:]

    # --------------------------------------------------
    # Add User
    # --------------------------------------------------

    @classmethod
    def add_user(cls, message):

        cls._append(

            role="user",

            content=message

        )

    # Backward compatibility

    add_user_message = add_user

    # --------------------------------------------------
    # Add Assistant
    # --------------------------------------------------

    @classmethod
    def add_assistant(cls, message):

        cls._append(

            role="assistant",

            content=message

        )

    # Backward compatibility

    add_assistant_message = add_assistant

    # --------------------------------------------------
    # Complete History
    # --------------------------------------------------

    @classmethod
    def history(cls):

        cls.initialize()

        return st.session_state[cls.SESSION_KEY]

    # --------------------------------------------------
    # Recent Messages
    # --------------------------------------------------

    @classmethod
    def recent(cls, count=8):

        cls.initialize()

        return st.session_state[cls.SESSION_KEY][-count:]

    # Backward compatibility

    latest = recent

    # --------------------------------------------------
    # Has Messages
    # --------------------------------------------------

    @classmethod
    def has_messages(cls):

        return len(cls.history()) > 0

    # --------------------------------------------------
    # Clear
    # --------------------------------------------------

    @classmethod
    def clear(cls):

        st.session_state[cls.SESSION_KEY] = []

    # --------------------------------------------------
    # Export Markdown
    # --------------------------------------------------

    @classmethod
    def export_markdown(cls):

        lines = []

        for msg in cls.history():

            role = "User" if msg["role"] == "user" else "DemandIQ"

            lines.append(f"## {role}")

            lines.append(msg["content"])

            lines.append("")

        return "\n".join(lines)

    # Backward compatibility

    transcript = export_markdown