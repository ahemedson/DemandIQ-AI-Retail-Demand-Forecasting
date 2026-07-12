import streamlit as st


def show():

    # --------------------------------------------------
    # Check Dataset
    # --------------------------------------------------

    if st.session_state.dataset is None:
        st.title("🔍 Data Explorer")
        st.info("👈 Upload a retail dataset from the sidebar to begin.")
        return

    loader = st.session_state.loader
    clean_df = st.session_state.dataset

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    st.title("🔍 Data Explorer")
    st.caption("Inspect and validate the uploaded retail dataset.")

    # --------------------------------------------------
    # Dataset Information
    # --------------------------------------------------

    st.subheader("📂 Dataset Information")

    summary = loader.get_dataset_summary()

    c1, c2, c3 = st.columns(3)

    c1.metric("Rows", summary["Rows"])
    c2.metric("Columns", summary["Columns"])
    c3.metric("Memory Usage", f"{summary['Memory Usage (MB)']} MB")

    st.divider()

    # --------------------------------------------------
    # Dataset Preview
    # --------------------------------------------------

    st.subheader("👀 Dataset Preview")

    st.dataframe(
        clean_df,
        use_container_width=True,
        height=400
    )

    st.divider()

    # --------------------------------------------------
    # Column Details
    # --------------------------------------------------

    with st.expander("📋 Column Details", expanded=False):

        st.dataframe(
            loader.get_column_details(),
            use_container_width=True
        )

    # --------------------------------------------------
    # Missing Values
    # --------------------------------------------------

    with st.expander("⚠ Missing Values", expanded=False):

        st.dataframe(
            loader.get_missing_values(),
            use_container_width=True
        )

    # --------------------------------------------------
    # Statistical Summary
    # --------------------------------------------------

    with st.expander("📊 Statistical Summary", expanded=False):

        st.dataframe(
            loader.get_statistics(),
            use_container_width=True
        )

    # --------------------------------------------------
    # Data Types
    # --------------------------------------------------

    with st.expander("🧾 Data Types", expanded=False):

        st.write(clean_df.dtypes)