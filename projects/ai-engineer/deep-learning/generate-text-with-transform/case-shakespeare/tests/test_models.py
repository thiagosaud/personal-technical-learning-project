import numpy as np
import tensorflow as tf

from src.core.model.transformer_block import TransformerBlock
from src.core.model.transformer_causal import TransformerCausal


def test_transformer_block_preserves_tensor_shape() -> None:
    block = TransformerBlock(embed_dim=8, num_heads=2, ff_dim=16, dropout_rate=0)
    inputs = tf.random.normal((2, 4, 8))

    outputs = block(inputs, training=False)

    assert tuple(outputs.shape) == (2, 4, 8)
    assert block.get_config()["num_heads"] == 2


def test_transformer_causal_returns_vocabulary_logits() -> None:
    model = TransformerCausal(
        vocab_size=12,
        seq_length=4,
        embed_dim=8,
        num_heads=2,
        ff_dim=16,
        num_layers=1,
        dropout_rate=0,
    )
    inputs = tf.constant([[1, 2, 3, 4]])

    outputs = model(inputs, training=False)

    assert tuple(outputs.shape) == (1, 4, 12)
    assert model.get_config()["seq_length"] == 4
    assert np.isfinite(outputs.numpy()).all()
