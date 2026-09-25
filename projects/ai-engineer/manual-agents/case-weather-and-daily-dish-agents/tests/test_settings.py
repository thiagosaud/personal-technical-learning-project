from pathlib import Path

from src.app.configs.settings import Settings


def test_settings_paths():
    """Validates that base directory and FAQ path are correctly resolved."""
    assert isinstance(Settings.BASE_DIR, Path)
    assert Settings.FAQ_PDF_PATH.endswith("The_Daily_Dish_FAQ.pdf")
    assert isinstance(Settings.SIMILARITY_THRESHOLD, float)
