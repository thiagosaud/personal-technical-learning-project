from unittest.mock import MagicMock, Mock, patch

import numpy as np
import pytest
import tensorflow as tf

from src.core.generation.text_generator import TextGenerator


@pytest.fixture
def generator() -> TextGenerator:
    vectorizer = Mock()
    vectorizer.get_vocabulary.return_value = ["", "[UNK]", "to", "be", "or"]
    return TextGenerator(model=Mock(), vectorizer=vectorizer, seq_length=4)


def test_generator_rejects_empty_vocabulary() -> None:
    vectorizer = Mock()
    vectorizer.get_vocabulary.return_value = []
    model = Mock()

    with pytest.raises(ValueError, match="vocabulary is empty"):
        TextGenerator(model=model, vectorizer=vectorizer, seq_length=4)


def test_temperature_must_be_positive(generator: TextGenerator) -> None:
    logits = tf.constant([1.0])
    with pytest.raises(ValueError, match="greater than zero"):
        generator._apply_temperature(logits, 0)


def test_top_k_leaves_logits_unchanged_when_k_is_out_of_range(generator: TextGenerator) -> None:
    logits = tf.constant([[1.0, 2.0, 3.0]])

    result = generator._top_k_filtering(logits, 0)

    np.testing.assert_allclose(result.numpy(), logits.numpy())


def test_generate_rejects_invalid_prompt_and_length(generator: TextGenerator) -> None:
    with pytest.raises(ValueError, match="non-empty prompt"):
        generator.generate("   ")
    with pytest.raises(ValueError, match="cannot be negative"):
        generator.generate("prompt", num_generate=-1)


def test_generate_returns_prompt_and_decoded_tokens(generator: TextGenerator) -> None:
    vectorizer_output = MagicMock()
    vectorizer_output.numpy.return_value = np.array([2, 3], dtype=np.int32)
    generator.vectorizer.return_value = vectorizer_output
    generator.model.return_value = tf.constant([[[0.0, 0.0, 8.0, 1.0, 0.0]]])

    with patch("src.core.generation.text_generator.tf.random.categorical", return_value=tf.constant([[3]])):
        result = generator.generate("to", num_generate=1, temperature=1.0, top_k=1)

    assert result == "to be"
    generator.model.assert_called_once()
