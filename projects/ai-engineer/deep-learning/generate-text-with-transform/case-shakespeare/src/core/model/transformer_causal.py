"""Causal decoder-only Transformer model used for text generation."""

from typing import Any

import numpy as np
import tensorflow as tf
from keras import Model
from keras.layers import Dense, Dropout, Embedding, LayerNormalization

from src.core.model.transformer_block import TransformerBlock


class TransformerCausal(Model):
    """A compact decoder-only Transformer trained to predict the next token."""

    def __init__(
        self,
        vocab_size: int,
        seq_length: int,
        embed_dim: int = 256,
        num_heads: int = 8,
        ff_dim: int = 1024,
        num_layers: int = 6,
        dropout_rate: float = 0.1,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.vocab_size = vocab_size
        self.seq_length = seq_length
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.num_layers = num_layers
        self.dropout_rate = dropout_rate

        self.token_embedding = Embedding(
            input_dim=vocab_size,
            output_dim=embed_dim,
            name="token_embedding",
        )

        self.positional_encoding = self._build_positional_encoding(seq_length, embed_dim)
        self.transformer_blocks = [
            TransformerBlock(
                embed_dim=embed_dim,
                num_heads=num_heads,
                ff_dim=ff_dim,
                dropout_rate=dropout_rate,
                name=f"transformer_block_{i}",
            )
            for i in range(num_layers)
        ]

        self.dropout = Dropout(dropout_rate)
        self.final_norm = LayerNormalization(epsilon=1e-6)
        self.output_dense = Dense(vocab_size, name="output_projection")

    def _build_positional_encoding(self, seq_length: int, embed_dim: int) -> tf.Tensor:
        """Create sinusoidal positional encodings following the standard Transformer formulation."""
        # Positional encodings let the model understand token order without relying on recurrence.
        positions = np.arange(seq_length)[:, np.newaxis]
        div_term = np.exp(np.arange(0, embed_dim, 2) * -(np.log(10000.0) / embed_dim))

        positional_encoding = np.zeros((seq_length, embed_dim))
        positional_encoding[:, 0::2] = np.sin(positions * div_term)
        positional_encoding[:, 1::2] = np.cos(positions * div_term)
        return tf.cast(positional_encoding[np.newaxis, ...], tf.float32)

    def call(self, inputs: tf.Tensor, training: bool = False) -> tf.Tensor:
        """Run a full forward pass and return vocabulary logits."""
        sequence_length = tf.shape(inputs)[1]

        # Embed tokens and add fixed positional information before the decoder stack.
        hidden_state = self.token_embedding(inputs)
        hidden_state *= tf.math.sqrt(tf.cast(self.embed_dim, tf.float32))
        hidden_state += self.positional_encoding[:, :sequence_length, :]
        hidden_state = self.dropout(hidden_state, training=training)

        # Apply the stacked causal transformer blocks to model long-range context.
        for block in self.transformer_blocks:
            hidden_state = block(hidden_state, training=training)

        hidden_state = self.final_norm(hidden_state)
        return self.output_dense(hidden_state)

    def get_config(self) -> dict[str, Any]:
        config = super().get_config()
        config.update(
            {
                "vocab_size": self.vocab_size,
                "seq_length": self.seq_length,
                "embed_dim": self.embed_dim,
                "num_heads": self.num_heads,
                "ff_dim": self.ff_dim,
                "num_layers": self.num_layers,
                "dropout_rate": self.dropout_rate,
            }
        )
        return config
