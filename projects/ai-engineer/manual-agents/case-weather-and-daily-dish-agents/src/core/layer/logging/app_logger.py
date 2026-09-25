import logging
import sys


class AppLogger:
    """Centralized application logger provider ensuring standard output format across components."""

    @staticmethod
    def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
        """
        Creates and configures a standard logger instance with a clean console formatter.

        Args:
            name (str): The module or component name for the logger context.
            level (int): The logging severity threshold level.

        Returns:
            logging.Logger: Fully configured logger instance.
        """
        logger = logging.getLogger(name)

        # Avoid duplicate handlers if logger was already initialized
        if logger.hasHandlers():
            return logger

        logger.setLevel(level)

        # Console stream handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Professional log formatter
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger
