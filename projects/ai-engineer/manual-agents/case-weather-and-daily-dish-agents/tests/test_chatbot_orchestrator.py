from src.core.domain.orchestrator.chatbot_orchestrator import ChatbotOrchestrator


def test_chatbot_orchestrator_flow():
    """Validates orchestrator initialization and response handling."""
    sample_faq = [{"question": "Where are you located?", "answer": "We are located in New York City."}]

    orchestrator = ChatbotOrchestrator(faq_data=sample_faq)

    # Test FAQ routing
    response = orchestrator.handle_question("Where is the restaurant?")
    assert response is not None
    assert isinstance(response, str)
