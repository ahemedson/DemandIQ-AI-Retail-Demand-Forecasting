import streamlit as st


def show_chat_input():
    """
    Display the DemandIQ Copilot chat input.

    Returns
    -------
    str | None
        The user's question if submitted,
        otherwise None.
    """

    question = st.chat_input(

        "Ask DemandIQ about your business, demand forecast or inventory..."

    )

    if question:

        question = question.strip()

        if question:

            return question

    return None