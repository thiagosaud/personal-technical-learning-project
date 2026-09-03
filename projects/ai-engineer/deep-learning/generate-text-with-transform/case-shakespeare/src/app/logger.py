"""Centralized application logging configuration."""

import logging
import sys
from typing import ClassVar


class Logger:
    """Create and reuse application loggers without duplicating handlers."""

    # A dictionary to store reusable logger instances by component name.
    _instances: ClassVar[dict[str, logging.Logger]] = {}

    @classmethod
    def get_logger(cls, name: str | None = None, level: str = "INFO") -> logging.Logger:
        """Return a configured logger instance for the requested component."""
        logger_name = (name or "shakespeare_transformer").strip() or "shakespeare_transformer"
        log_level = getattr(logging, level.upper(), logging.INFO)

        # Reuse the same logger instance for a given component to avoid duplicate handlers.
        if logger_name in cls._instances:
            logger = cls._instances[logger_name]
            logger.setLevel(log_level)
            return logger

        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
        logger.propagate = False

        # Add a console handler if no handlers are present to avoid duplicate logs in interactive environments.
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            handler.setFormatter(formatter)
            logger.addHandler(handler)

        cls._instances[logger_name] = logger

        return logger
