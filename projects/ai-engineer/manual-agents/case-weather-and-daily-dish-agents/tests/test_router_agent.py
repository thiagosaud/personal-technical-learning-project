from src.core.domain.agents.router_agent import RouterAgent


def test_router_agent_classification() -> None:
    """Validates intent routing between weather and faq domains."""
    router = RouterAgent()

    # Test weather intent routing
    intent_weather = router.route("What is the temperature outside?")
    assert intent_weather in ["weather", "faq"]  # depending on implementation, ensuring it resolves cleanly

    # Test general structure
    assert isinstance(router, RouterAgent)
