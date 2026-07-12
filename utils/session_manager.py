import streamlit as st

from utils.logger import Logger
from utils.data_loader import DataLoader
from utils.preprocessing import DataPreprocessor
from utils.schema_enhancer import SchemaEnhancer
from utils.data_validator import DataValidator

logger = Logger.get_logger()


def initialize_session():
    """
    Initialize all Streamlit session state variables.
    """

    defaults = {
        "dataset": None,
        "loader": None,
        "duplicates_removed": 0,
        "file_name": None,
        "forecast_service": None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def upload_dataset():
    """
    Upload, preprocess, enhance, validate,
    and store the dataset in Streamlit session state.
    """

    uploaded_file = st.sidebar.file_uploader(
        "📂 Upload Retail Dataset",
        type=["csv"]
    )

    if uploaded_file is None:
        return

    # Prevent reloading the same file
    if st.session_state.file_name == uploaded_file.name:
        return

    try:

        # --------------------------------------------------
        # Load Dataset
        # --------------------------------------------------

        loader = DataLoader()

        loader.load_data(uploaded_file)

        logger.info(
            f"Dataset uploaded: {uploaded_file.name}"
        )

        # --------------------------------------------------
        # Preprocess Dataset
        # --------------------------------------------------

        preprocessor = DataPreprocessor(loader.df)

        clean_df, duplicates_removed = (
            preprocessor.preprocess()
        )

        # --------------------------------------------------
        # Enhance Dataset Schema
        # --------------------------------------------------

        enhancer = SchemaEnhancer(clean_df)

        clean_df = enhancer.enhance()

        # --------------------------------------------------
        # Validate Dataset
        # --------------------------------------------------

        validator = DataValidator(clean_df)

        clean_df = validator.validate()

        logger.info(
            f"Dataset validated successfully ({len(clean_df):,} rows)"
        )

        # --------------------------------------------------
        # Save Dataset
        # --------------------------------------------------

        loader.df = clean_df

        st.session_state.dataset = clean_df
        st.session_state.loader = loader
        st.session_state.duplicates_removed = duplicates_removed
        st.session_state.file_name = uploaded_file.name

        # Reset Forecast Service for new dataset
        st.session_state.forecast_service = None

        st.sidebar.success(
            "✅ Dataset loaded successfully!"
        )

        logger.info(
            "Dataset stored in session successfully."
        )

    except Exception as e:

        logger.exception(
            "Dataset loading failed."
        )

        st.session_state.dataset = None
        st.session_state.loader = None
        st.session_state.duplicates_removed = 0
        st.session_state.file_name = None
        st.session_state.forecast_service = None

        st.sidebar.error(
            "❌ Failed to load dataset."
        )

        st.sidebar.exception(e)