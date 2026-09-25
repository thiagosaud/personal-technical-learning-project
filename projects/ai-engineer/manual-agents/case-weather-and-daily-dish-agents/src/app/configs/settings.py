import os
from pathlib import Path


class Settings:
    """Centralized configuration class holding environment variables and system constants."""

    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "YOUR_API_KEY_HERE")
    WEATHER_URL: str = "https://api.openweathermap.org/data/2.5/weather"
    RESTAURANT_CITY: str = "New York"

    # Path resolution for src/app/configs/settings.py -> configs -> app -> src -> root
    BASE_DIR: Path = Path(__file__).resolve().parents[3]
    FAQ_PDF_PATH: str = str(BASE_DIR / "data" / "raw" / "The_Daily_Dish_FAQ.pdf")

    SIMILARITY_THRESHOLD: float = 0.08
