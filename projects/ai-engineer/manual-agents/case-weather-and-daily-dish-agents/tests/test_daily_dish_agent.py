from unittest.mock import patch

import numpy as np

from src.core.domain.agents.daily_dish_agent import DailyDishAgent


def test_daily_dish_agent_matching() -> None:
    """Verifies that the agent returns the highest-scoring FAQ answer."""
    sample_faq = [
        {"question": "What are your opening hours?", "answer": "We are open from 9am to 10pm."},
        {"question": "Do you offer vegan options?", "answer": "Yes, we have several vegan dishes."},
    ]

    agent = DailyDishAgent(faq_data=sample_faq, threshold=0.01)

    # Force a deterministic ranking without touching external ML libraries
    with (
        patch.object(
            agent,
            "_vectorizer",
            wraps=agent._vectorizer,
        ),
        patch(
            "src.core.domain.agents.daily_dish_agent.cosine_similarity",
            return_value=np.array([[0.95, 0.10]]),
        ),
    ):
        response = agent.answer("What time do you open?")
        assert response == "We are open from 9am to 10pm."


def test_daily_dish_agent_below_threshold() -> None:
    """Ensures None is returned when no FAQ exceeds the similarity threshold."""
    sample_faq = [
        {"question": "What are your opening hours?", "answer": "We are open from 9am to 10pm."},
    ]
    agent = DailyDishAgent(faq_data=sample_faq, threshold=0.99)

    with patch(
        "src.core.domain.agents.daily_dish_agent.cosine_similarity",
        return_value=np.array([[0.05]]),
    ):
        assert agent.answer("completely unrelated query") is None
