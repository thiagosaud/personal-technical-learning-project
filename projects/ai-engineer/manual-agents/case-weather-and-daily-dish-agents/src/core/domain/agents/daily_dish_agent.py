from __future__ import annotations

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.core.layer.logging.app_logger import AppLogger


class DailyDishAgent:
    """Performs semantic FAQ matching using TF-IDF vectorization and cosine similarity."""

    def __init__(self, faq_data: list[dict[str, str]], threshold: float = 0.08) -> None:
        """
        Args:
            faq_data: List of structured question-answer dictionaries.
            threshold: Minimum cosine-similarity score required for a valid match
                       (default matches Settings.SIMILARITY_THRESHOLD).
        """
        self._logger = AppLogger.get_logger(self.__class__.__name__)
        self._questions = [item["question"] for item in faq_data]
        self._answers = [item["answer"] for item in faq_data]
        self._threshold = threshold

        self._vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
        )
        self._doc_matrix = self._vectorizer.fit_transform(self._questions)
        self._logger.info(
            "TF-IDF matrix built for %d FAQ entries (vocabulary size=%d).",
            len(self._questions),
            len(self._vectorizer.vocabulary_),
        )

    def answer(self, processed_query: str) -> str | None:
        """
        Returns the most similar FAQ answer or ``None`` when the score falls
        below the configured threshold.
        """
        if not processed_query.strip():
            self._logger.warning("Empty query received; returning None.")
            return None

        query_vec = self._vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vec, self._doc_matrix).flatten()

        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])

        self._logger.debug(
            "TF-IDF cosine similarity: %.4f (threshold=%.2f)",
            best_score,
            self._threshold,
        )

        if best_score < self._threshold:
            self._logger.info("Similarity below threshold; falling back.")
            return None

        return self._answers[best_idx]
