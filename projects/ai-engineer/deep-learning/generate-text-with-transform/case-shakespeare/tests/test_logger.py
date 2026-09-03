import logging

from src.app.logger import Logger


def test_get_logger_reuses_named_instance() -> None:
    first = Logger.get_logger("test.logger", "DEBUG")
    second = Logger.get_logger("test.logger", "WARNING")

    assert first is second
    assert second.level == logging.WARNING
    assert len(second.handlers) == 1


def test_get_logger_uses_default_name_for_blank_name() -> None:
    logger = Logger.get_logger("   ")

    assert logger.name == "shakespeare_transformer"
    assert logger.propagate is False
