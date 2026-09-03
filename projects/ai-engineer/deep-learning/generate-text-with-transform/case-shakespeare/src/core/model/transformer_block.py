"""Transformer decoder block used by the causal language model."""

from typing import Any

import tensorflow as tf
from keras import Sequential
from keras.layers import Dense, Dropout, Layer, LayerNormalization, MultiHeadAttention


class TransformerBlock(Layer):
    """A single decoder block with causal self-attention and feed-forward network."""

    def __init__(
        self,
        embed_dim: int,
        num_heads: int,
        ff_dim: int,
        dropout_rate: float = 0.1,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.dropout_rate = dropout_rate

        self.attention = MultiHeadAttention(
            num_heads=num_heads,
            key_dim=embed_dim // num_heads,
            dropout=dropout_rate,
        )

        self.feed_forward = Sequential(
            [
                Dense(ff_dim, activation="gelu"),
                Dropout(dropout_rate),
                Dense(embed_dim),
            ]
        )

        self.layer_norm_1 = LayerNormalization(epsilon=1e-6)
        self.layer_norm_2 = LayerNormalization(epsilon=1e-6)
        self.dropout_1 = Dropout(dropout_rate)
        self.dropout_2 = Dropout(dropout_rate)

    def call(self, inputs: tf.Tensor, training: bool = False) -> tf.Tensor:
        """Execute the residual attention + feed-forward pass."""
        # Normalize the incoming sequence before the masked attention block.
        normalized = self.layer_norm_1(inputs)
        attention_output = self.attention(
            query=normalized,
            value=normalized,
            key=normalized,
            use_causal_mask=True,
            training=training,
        )
        attention_output = self.dropout_1(attention_output, training=training)
        residual_output = inputs + attention_output

        # Apply the second residual branch with the pointwise feed-forward network.
        normalized = self.layer_norm_2(residual_output)
        feed_forward_output = self.feed_forward(normalized, training=training)
        feed_forward_output = self.dropout_2(feed_forward_output, training=training)

        return residual_output + feed_forward_output

    def get_config(self) -> dict[str, Any]:
        config = super().get_config()
        config.update(
            {
                "embed_dim": self.embed_dim,
                "num_heads": self.num_heads,
                "ff_dim": self.ff_dim,
                "dropout_rate": self.dropout_rate,
            }
        )
        return config
