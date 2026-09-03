from pathlib import Path

import numpy as np
import pytest
from keras.layers import TextVectorization

from src.core.data_loader import TextLoader
from src.core.dataset_builder import DatasetBuilder


def test_text_loader_reads_utf8_file(tmp_path: Path) -> None:
    path = tmp_path / "corpus.txt"
    path.write_text("To be", encoding="utf-8")

    assert TextLoader(path).load() == "To be"


def test_text_loader_raises_for_missing_file(tmp_path: Path) -> None:
    loader = TextLoader(tmp_path / "missing.txt")
    with pytest.raises(FileNotFoundError, match="not found"):
        loader.load()


def test_dataset_builder_creates_shifted_sequences() -> None:
    builder = DatasetBuilder(vocab_size=20, seq_length=3, batch_size=1)
    features, labels = builder._create_sequences(np.array([1, 2, 3, 4, 5]))

    np.testing.assert_array_equal(features, [[1, 2, 3], [2, 3, 4]])
    np.testing.assert_array_equal(labels, [[2, 3, 4], [3, 4, 5]])


def test_dataset_builder_rejects_short_corpus() -> None:
    builder = DatasetBuilder(vocab_size=20, seq_length=4, batch_size=1)

    with pytest.raises(ValueError, match="too short"):
        builder._create_sequences(np.array([1, 2, 3, 4]))


def test_prepare_vectorizer_rejects_blank_text() -> None:
    builder = DatasetBuilder(vocab_size=20, seq_length=3, batch_size=1)

    with pytest.raises(ValueError, match="empty"):
        builder.prepare_vectorizer("   ")


def test_create_datasets_returns_batched_datasets() -> None:
    builder = DatasetBuilder(vocab_size=20, seq_length=2, batch_size=1, validation_split=0.5)
    vectorizer = TextVectorization(max_tokens=20, output_mode="int")
    vectorizer.adapt(["one two three four five"])

    train_dataset, validation_dataset = builder.create_datasets("one two three four five", vectorizer)
    train_batch = next(iter(train_dataset))
    validation_batch = next(iter(validation_dataset))

    assert tuple(train_batch[0].shape) == (1, 2)
    assert tuple(validation_batch[1].shape) == (1, 2)
