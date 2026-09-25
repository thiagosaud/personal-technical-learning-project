from src.core.domain.agents.daily_dish_agent import DailyDishAgent


def test_daily_dish_agent_matching():
    """Tests semantic matching for the FAQ agent."""
    sample_faq = [
        {"question": "What are your opening hours?", "answer": "We are open from 9am to 10pm."},
        {"question": "Do you offer vegan options?", "answer": "Yes, we have several vegan dishes."},
    ]

    agent = DailyDishAgent(faq_data=sample_faq, threshold=0.30)

    # Test English match
    response = agent.answer("What time do you open?")
    assert response == "We are open from 9am to 10pm."

    # Test cross-lingual match (Portuguese)
    response_pt = agent.answer("Vocês têm opções veganas?")
    assert response_pt == "Yes, we have several vegan dishes."
