import re

from src.core.layer.logging.app_logger import AppLogger


class QueryProcessor:
    """Preprocesses, sanitizes, and expands user queries using domain-specific contextual synonyms."""

    def __init__(self) -> None:
        """Initializes synonym dictionary for semantic query enrichment."""
        self._logger = AppLogger.get_logger(self.__class__.__name__)
        self._synonyms = {
            "location": "located address",
            "where": "located address",
            "reservation": "reserve booking",
            "menu": "food dishes",
            "fish": "seafood",
        }

    def process(self, query: str) -> str:
        """
        Normalizes text, strips special characters, and appends configured synonyms.

        Args:
            query (str): Raw user query string.

        Returns:
            str: Processed and expanded query string.
        """
        normalized = query.lower()
        normalized = re.sub(r"[^\w\s]", "", normalized)

        for key, synonym_values in self._synonyms.items():
            if key in normalized:
                normalized += f" {synonym_values}"
                self._logger.debug("Applied synonym expansion for keyword '%s'", key)

        return normalized
