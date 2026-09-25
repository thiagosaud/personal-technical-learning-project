from src.core.layer.logging.app_logger import AppLogger


class RouterAgent:
    """Evaluates user requests and routes them to the correct specialized domain agent."""

    def __init__(self) -> None:
        """Initializes domain-specific keyword mapping rules."""
        self._logger = AppLogger.get_logger(self.__class__.__name__)
        self._weather_keywords: list[str] = [
            "weather",
            "rain",
            "raining",
            "forecast",
            "temperature",
            "hot",
            "cold",
            "humidity",
        ]

    def route(self, query: str) -> str:
        """
        Analyzes query text to determine intent domain ('weather' or 'daily_dish').

        Args:
            query (str): Input user text.

        Returns:
            str: Target agent route destination identifier.
        """
        normalized_query = query.lower()
        for word in self._weather_keywords:
            if word in normalized_query:
                self._logger.debug("Keyword match found ('%s'). Routing to 'weather' domain.", word)
                return "weather"

        self._logger.debug("No specialized routing keywords matched. Routing to 'daily_dish' domain.")
        return "daily_dish"
