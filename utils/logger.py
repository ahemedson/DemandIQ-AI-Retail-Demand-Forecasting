import logging
from pathlib import Path


class Logger:
    """
    Centralized application logger.
    """

    _logger = None

    @classmethod
    def get_logger(cls):

        if cls._logger is not None:
            return cls._logger

        # -------------------------------
        # Create logs directory
        # -------------------------------

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "demandiq.log"

        # -------------------------------
        # Configure Logger
        # -------------------------------

        logger = logging.getLogger("DemandIQ")

        logger.setLevel(logging.INFO)

        if not logger.handlers:

            formatter = logging.Formatter(

                "%(asctime)s | %(levelname)s | %(message)s"

            )

            file_handler = logging.FileHandler(log_file)

            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

        cls._logger = logger

        return logger