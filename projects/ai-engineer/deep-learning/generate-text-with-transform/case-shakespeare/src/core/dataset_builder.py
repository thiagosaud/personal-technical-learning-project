"""Dataset creation utilities for next-token language modeling."""

import numpy as np
import tensorflow as tf
from keras.layers import TextVectorization

from src.app.logger import Logger


class DatasetBuilder:
    """Create vectorized sequences and tf.data pipelines for autoregressive training."""

    def __init__(
        self,
        vocab_size: int,
        seq_length: int,
        batch_size: int,
        buffer_size: int = 10_000,
        validation_split: float = 0.05,
    ) -> None:
        """Initialize the tokenization and batching configuration used during training."""
        self.vocab_size = vocab_size
        self.seq_length = seq_length
        self.batch_size = batch_size
        self.buffer_size = buffer_size
        self.validation_split = validation_split
        self.logger = Logger().get_logger(name="core.dataset_builder", level="INFO")

    def prepare_vectorizer(self, text: str) -> TextVectorization:
        """Build a TextVectorization layer trained on the corpus."""
        if not text or not text.strip():
            raise ValueError("The input text is empty; dataset creation cannot continue.")

        # Build a token-level vectorizer that learns the corpus vocabulary before training.
        vectorizer = TextVectorization(
            max_tokens=self.vocab_size,
            output_mode="int",
            standardize="lower_and_strip_punctuation",
        )

        text_dataset = tf.data.Dataset.from_tensor_slices([text]).batch(1)
        vectorizer.adapt(text_dataset)

        actual_vocab_size = len(vectorizer.get_vocabulary())
        self.logger.info("Vectorizer adapted | vocabulary size = %d", actual_vocab_size)
        return vectorizer

    def _create_sequences(self, token_ids: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Generate input-target pairs using a sliding window over the token sequence."""
        if len(token_ids) <= self.seq_length:
            raise ValueError(
                "The corpus is too short for the configured sequence length. "
                f"Need > {self.seq_length} tokens, got {len(token_ids)}."
            )

        inputs: list[np.ndarray] = []
        targets: list[np.ndarray] = []

        for index in range(len(token_ids) - self.seq_length):
            inputs.append(token_ids[index : index + self.seq_length])
            targets.append(token_ids[index + 1 : index + self.seq_length + 1])

        return np.array(inputs, dtype=np.int32), np.array(targets, dtype=np.int32)

    def create_datasets(
        self,
        text: str,
        vectorizer: TextVectorization,
    ) -> tuple[tf.data.Dataset, tf.data.Dataset]:
        """Return train and validation datasets in tf.data format."""
        token_ids = vectorizer([text])[0].numpy()
        self.logger.info("Corpus vectorized | total tokens = %s", f"{len(token_ids):,}")

        features, labels = self._create_sequences(token_ids)
        self.logger.info("Created %s sequences of length %d", f"{len(features):,}", self.seq_length)

        split_index = int(len(features) * (1.0 - self.validation_split))
        train_features, train_labels = features[:split_index], labels[:split_index]
        val_features, val_labels = features[split_index:], labels[split_index:]

        train_dataset = self._make_dataset(train_features, train_labels, shuffle=True)
        val_dataset = self._make_dataset(val_features, val_labels, shuffle=False)

        self.logger.info(
            "Datasets ready | train batches ≈ %d | val batches ≈ %d",
            split_index // self.batch_size,
            (len(features) - split_index) // self.batch_size,
        )

        return train_dataset, val_dataset

    def _make_dataset(
        self,
        features: np.ndarray,
        labels: np.ndarray,
        shuffle: bool = False,
    ) -> tf.data.Dataset:
        """Convert arrays to batched tf.data datasets."""
        if features.size == 0 or labels.size == 0:
            raise ValueError("Dataset creation encountered an empty feature or label array.")

        dataset = tf.data.Dataset.from_tensor_slices((features, labels))

        if shuffle:
            dataset = dataset.shuffle(self.buffer_size, reshuffle_each_iteration=True)

        dataset = dataset.batch(self.batch_size, drop_remainder=True)
        dataset = dataset.prefetch(tf.data.AUTOTUNE)
        return dataset
