from src.core.layer.logging.app_logger import AppLogger


def test_app_logger_initialization() -> None:
    """Validates that AppLogger returns a properly configured logger instance."""
    logger_name = "TestLoggerModule"
    logger = AppLogger.get_logger(logger_name)

    assert logger is not None
    assert logger.name == logger_name
