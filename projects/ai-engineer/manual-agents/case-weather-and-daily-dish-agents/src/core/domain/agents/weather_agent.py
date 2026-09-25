import requests

from src.core.layer.logging.app_logger import AppLogger
from src.core.layer.memory.memory_agent import MemoryAgent


class WeatherAgent:
    """Handles external weather data fetching via OpenWeather API and manages historical context."""

    def __init__(self, api_key: str, memory_agent: MemoryAgent, url: str) -> None:
        """
        Args:
            api_key (str): OpenWeather authentication key.
            memory_agent (MemoryAgent): Shared memory instance for tracking prior temperatures.
            url (str): Target API endpoint URL.
        """
        self._api_key = api_key
        self._memory = memory_agent
        self._url = url
        self._logger = AppLogger.get_logger(self.__class__.__name__)

    def answer(self, city: str) -> str:
        """
        Fetches current weather data for a given city and compares it with previous memory state.

        Args:
            city (str): Target city name.

        Returns:
            str: Natural language formatted weather report with contextual comparisons.
        """
        params = {"q": city, "appid": self._api_key, "units": "metric"}

        try:
            self._logger.info("Fetching weather data for city: '%s'", city)
            response = requests.get(self._url, params=params, timeout=10)

            if response.status_code != 200:
                self._logger.warning("Weather API returned status code %d", response.status_code)
                return "I couldn't retrieve the weather right now."

            data = response.json()
            previous_data = self._memory.recall(city)
            self._memory.store(city, data["main"])

            description = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            result = f"The current weather in {city} is {description} with a temperature of {temp}°C."

            if previous_data:
                result += f" Earlier it was {previous_data['temp']}°C."
                self._logger.debug("Compared with historical memory. Previous temp was %s°C", previous_data["temp"])

            return result
        except requests.RequestException as e:
            self._logger.error("Connection error while calling OpenWeather API: %s", e)
            return "I couldn't connect to the weather service right now."
