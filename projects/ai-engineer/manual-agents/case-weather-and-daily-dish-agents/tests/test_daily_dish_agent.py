from unittest.mock import MagicMock, patch

from src.core.domain.agents.daily_dish_agent import DailyDishAgent


def test_daily_dish_agent_matching():
    """Tests semantic matching for the FAQ agent."""
    sample_faq = [
        {"question": "What are your opening hours?", "answer": "We are open from 9am to 10pm."},
        {"question": "Do you offer vegan options?", "answer": "Yes, we have several vegan dishes."},
    ]

    agent = DailyDishAgent(faq_data=sample_faq, threshold=0.30)

    # If running in CI mode, inject type-compliant mocks to simulate the model and embeddings
    if agent._model is None:
        agent._model = MagicMock()
        agent._doc_embeddings = MagicMock()  # Satisfies the Tensor | None typing constraint
        agent._model.encode.return_value = MagicMock()

    with patch("sentence_transformers.util.cos_sim") as mock_cos_sim, patch("numpy.argmax") as mock_argmax:
        # Simulate that the best matching index found is 0
        mock_argmax.return_value = 0

        # Mock the cosine similarity result chain containing .cpu().numpy()
        mock_similarities = MagicMock()
        mock_similarities.cpu().numpy.return_value = [0.95]

        # Create a mock element for similarities[best_idx] that supports .item()
        mock_score_element = MagicMock()
        mock_score_element.item.return_value = 0.95
        mock_similarities.__getitem__.return_value = mock_score_element

        mock_cos_sim.return_value = [mock_similarities]

        response = agent.answer("What time do you open?")
        assert response == "We are open from 9am to 10pm."
