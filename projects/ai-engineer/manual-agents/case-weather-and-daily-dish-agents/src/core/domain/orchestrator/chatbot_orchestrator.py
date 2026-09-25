from src.app.configs.settings import Settings
from src.core.domain.agents.daily_dish_agent import DailyDishAgent
from src.core.domain.agents.router_agent import RouterAgent
from src.core.domain.agents.weather_agent import WeatherAgent
from src.core.layer.logging.app_logger import AppLogger
from src.core.layer.memory.memory_agent import MemoryAgent
from src.core.layer.processor.query_processor import QueryProcessor


class ChatbotOrchestrator:
    """Coordinates dependency injection and manages the core conversational dispatch pipeline."""

    def __init__(self, faq_data: list) -> None:
        """
        Args:
            faq_data (list): Parsed FAQ dataset required by the DailyDish agent.
        """
        self._logger = AppLogger.get_logger(self.__class__.__name__)
        self._memory = MemoryAgent()
        self._query_processor = QueryProcessor()
        self._router = RouterAgent()

        self._weather_agent = WeatherAgent(
            api_key=Settings.WEATHER_API_KEY, memory_agent=self._memory, url=Settings.WEATHER_URL
        )
        self._daily_dish_agent = DailyDishAgent(faq_data=faq_data, threshold=Settings.SIMILARITY_THRESHOLD)
        self._logger.info("Chatbot orchestrator successfully initialized with all dependencies.")

    def handle_question(self, user_question: str) -> str:
        """
        Orchestrates routing, preprocessing, agent execution, and fallback handling.

        Args:
            user_question (str): Raw string input from user.

        Returns:
            str: Generated conversational response.
        """
        route = self._router.route(user_question)
        processed_query = self._query_processor.process(user_question)

        self._logger.info("Handling question via route target: '%s'", route)

        if route == "weather":
            return self._weather_agent.answer(Settings.RESTAURANT_CITY)

        answer = self._daily_dish_agent.answer(processed_query)
        if answer:
            return answer

        return "I'm not sure about that. Please ask a question related to The Daily Dish."
