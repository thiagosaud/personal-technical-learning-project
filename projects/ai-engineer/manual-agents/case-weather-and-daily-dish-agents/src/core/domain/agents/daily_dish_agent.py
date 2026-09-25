import numpy as np
from sentence_transformers import SentenceTransformer, util

from src.core.layer.logging.app_logger import AppLogger


class DailyDishAgent:
    """Performs native multilingual semantic FAQ matching using Sentence Transformers and Dense Embeddings."""

    def __init__(self, faq_data: list[dict[str, str]], threshold: float = 0.60) -> None:
        """
        Args:
            faq_data (List[Dict[str, str]]): List of structured question-answer dictionaries.
            threshold (float): Minimum cosine similarity score required for a valid cross-lingual match.
        """
        self._logger = AppLogger.get_logger(self.__class__.__name__)
        self._questions = [item["question"] for item in faq_data]
        self._answers = [item["answer"] for item in faq_data]
        self._threshold = threshold

        self._logger.info("Loading multilingual sentence transformer model (intfloat/multilingual-e5-small)...")
        # Load lightweight public multilingual model
        self._model = SentenceTransformer("intfloat/multilingual-e5-small")

        self._logger.info("Encoding FAQ dataset questions into dense vector embeddings...")
        # E5 models recommend prefixing passages for optimal retrieval
        prefixed_questions = [f"passage: {q}" for q in self._questions]
        self._doc_embeddings = self._model.encode(prefixed_questions, convert_to_tensor=True)

    def answer(self, processed_query: str) -> str | None:
        """
        Finds and returns the most semantically relevant answer for a user query in any language.

        Args:
            processed_query (str): Cleaned and normalized user query string.

        Returns:
            Optional[str]: Matching answer text or None if confidence score falls below threshold.
        """
        # E5 models recommend prefixing queries with 'query: '
        formatted_query = f"query: {processed_query}"
        query_embedding = self._model.encode(formatted_query, convert_to_tensor=True)

        similarities = util.cos_sim(query_embedding, self._doc_embeddings)[0]

        best_idx = int(np.argmax(similarities.cpu().numpy()))
        best_score = float(similarities[best_idx].item())

        self._logger.debug(
            "Calculated multilingual similarity score: %.4f (Threshold: %.2f)", best_score, self._threshold
        )

        if best_score < self._threshold:
            self._logger.info("Query similarity below multilingual threshold. Falling back to default message.")
            return None

        return self._answers[best_idx]
