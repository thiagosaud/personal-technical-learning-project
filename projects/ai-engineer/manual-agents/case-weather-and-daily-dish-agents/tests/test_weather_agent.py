from unittest.mock import MagicMock, patch

from src.core.domain.agents.weather_agent import WeatherAgent
from src.core.layer.memory.memory_agent import MemoryAgent


@patch("src.core.domain.agents.weather_agent.requests.get")
def test_weather_agent_response(mock_get: MagicMock) -> None:
    """Validates weather agent response structure using a mocked API response."""
    # Mock the OpenWeather API network response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"weather": [{"description": "clear sky"}], "main": {"temp": 22.5}}
    mock_get.return_value = mock_response

    # Instantiate required dependencies
    memory = MemoryAgent(max_history=3)
    agent = WeatherAgent(
        api_key="dummy_api_key", memory_agent=memory, url="https://api.openweathermap.org/data/2.5/weather"
    )

    # Call the correct method name: 'answer'
    response = agent.answer("London")

    assert isinstance(response, str)
    assert "London" in response
    assert "clear sky" in response
    assert "22.5°C" in response
