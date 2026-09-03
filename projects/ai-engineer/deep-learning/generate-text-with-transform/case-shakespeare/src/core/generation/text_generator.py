"""Text generation utilities with temperature and top-k sampling."""

import numpy as np
import tensorflow as tf
from keras.layers import TextVectorization

from src.app.logger import Logger
from src.core.model.transformer_causal import TransformerCausal

logger = Logger().get_logger(name="core.text_generator", level="INFO")


class TextGenerator:
    """Generate autoregressive text using a trained causal transformer."""

    def __init__(
        self,
        model: TransformerCausal,
        vectorizer: TextVectorization,
        seq_length: int,
    ) -> None:
        """Store the model, tokenizer, and sequence constraints used during inference."""
        self.model = model
        self.vectorizer = vectorizer
        self.seq_length = seq_length
        self.vocabulary = vectorizer.get_vocabulary()

        if not self.vocabulary:
            raise ValueError("The tokenizer vocabulary is empty; generation cannot proceed.")

    def _sanitize_for_log(self, value: object) -> str:
        """Return a single-line string safe to include in log entries."""
        return str(value).replace("\r", "").replace("\n", "")

    def _apply_temperature(self, logits: tf.Tensor, temperature: float) -> tf.Tensor:
        """Apply temperature scaling to the logits to control randomness."""
        if temperature <= 0:
            raise ValueError("Temperature must be greater than zero.")
        return logits / temperature

    def _top_k_filtering(self, logits: tf.Tensor, k: int) -> tf.Tensor:
        """Keep only the k most likely next tokens."""
        vocab_size = logits.shape[-1]
        if vocab_size is None:
            raise ValueError("logits tensor has no known vocabulary dimension")

        if k <= 0 or k >= vocab_size:
            return logits

        top_values, _ = tf.math.top_k(logits, k=k)
        min_top_value = top_values[:, -1]
        masked_logits = tf.fill(tf.shape(logits), -1e9)

        return tf.where(logits < tf.expand_dims(min_top_value, axis=-1), masked_logits, logits)

    def generate(
        self,
        start_string: str,
        num_generate: int = 300,
        temperature: float = 0.75,
        top_k: int = 40,
    ) -> str:
        """Generate text by repeatedly sampling the next token."""
        if not start_string or not start_string.strip():
            raise ValueError("A non-empty prompt is required to generate text.")
        if num_generate < 0:
            raise ValueError("The number of generated tokens cannot be negative.")

        # Convert the prompt into token IDs and stabilize the sequence length expected by the model.
        input_tokens = self.vectorizer([start_string])[0].numpy()

        if len(input_tokens) < self.seq_length:
            padding = np.zeros(self.seq_length - len(input_tokens), dtype=np.int32)
            input_tokens = np.concatenate([padding, input_tokens])
        else:
            input_tokens = input_tokens[-self.seq_length :]

        input_tokens = tf.convert_to_tensor(input_tokens[np.newaxis, :])
        generated_ids: list[int] = []

        # Generate one token at a time until the requested output length is reached.
        for step in range(num_generate):
            logits = self.model(input_tokens, training=False)
            next_token_logits = logits[0, -1, :]

            next_token_logits = self._apply_temperature(next_token_logits, temperature)
            next_token_logits = self._top_k_filtering(next_token_logits[tf.newaxis, :], top_k)[0]
            next_token = tf.random.categorical(next_token_logits[tf.newaxis, :], num_samples=1)[0, 0].numpy()

            generated_ids.append(int(next_token))
            input_tokens = tf.concat([input_tokens, [[next_token]]], axis=1)
            input_tokens = input_tokens[:, -self.seq_length :]

            if step % max(1, num_generate // 10) == 0:
                logger.debug("Generated token %d/%d during sampling", step + 1, num_generate)

        generated_words: list[str] = []
        for token_id in generated_ids:
            if 0 <= token_id < len(self.vocabulary):
                word = self.vocabulary[token_id]
                if word and word not in {"", "[UNK]"}:
                    generated_words.append(word)

        safe_temperature = self._sanitize_for_log(temperature)
        safe_top_k = self._sanitize_for_log(top_k)
        logger.info(
            "Generated %d tokens with temperature %s and top_k=%s",
            num_generate,
            safe_temperature,
            safe_top_k,
        )
        return start_string + " " + " ".join(generated_words)
