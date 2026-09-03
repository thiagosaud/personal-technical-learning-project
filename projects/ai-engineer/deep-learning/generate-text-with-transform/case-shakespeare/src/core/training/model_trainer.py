"""Training orchestration for the causal Transformer model."""

from pathlib import Path
from typing import Any

import tensorflow as tf
from keras.callbacks import (
    Callback,
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
    TensorBoard,
)
from keras.optimizers import AdamW

from src.app.logger import Logger
from src.core.model.transformer_causal import TransformerCausal

logger = Logger().get_logger(name="core.model_trainer", level="INFO")


class ModelTrainer:
    """Handle compilation, checkpointing, and execution of the training loop."""

    PROJECT_ROOT = Path(__file__).resolve().parents[3]

    def __init__(self, config: dict[str, Any]) -> None:
        """Store the configuration blocks used by the training pipeline."""
        # Keep paths and hyperparameters centered on the loaded YAML configuration.
        self.config = config
        self.model_cfg = config["model"]
        self.train_cfg = config["training"]
        self.data_cfg = config["data"]

        # Resolve training artifacts against the project root so checkpoints and logs are stored outside src.
        self.checkpoint_dir = self._resolve_path(self.train_cfg["checkpoint_dir"])
        self.log_dir = self._resolve_path(self.train_cfg["log_dir"])
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        logger.info("Training artifacts directory: %s", self.checkpoint_dir)
        logger.info("TensorBoard log directory: %s", self.log_dir)

    def _resolve_path(self, value: str | Path) -> Path:
        """Resolve relative paths against the project root."""
        path = Path(value)
        if path.is_absolute():
            return path
        return (self.PROJECT_ROOT / path).resolve()

    def build_model(self, vocab_size: int) -> TransformerCausal:
        """Instantiate and warm up the transformer model."""
        # Construct the model architecture and run a single warmup call to ensure the graph is valid before training.
        model = TransformerCausal(
            vocab_size=vocab_size,
            seq_length=self.data_cfg["seq_length"],
            embed_dim=self.model_cfg["embed_dim"],
            num_heads=self.model_cfg["num_heads"],
            ff_dim=self.model_cfg["ff_dim"],
            num_layers=self.model_cfg["num_layers"],
            dropout_rate=self.model_cfg["dropout_rate"],
        )

        dummy = tf.random.uniform((1, self.data_cfg["seq_length"]), maxval=vocab_size, dtype=tf.int32)
        _ = model(dummy)

        logger.info("Model built successfully")
        model.summary(print_fn=logger.info)
        return model

    def compile_model(self, model: TransformerCausal) -> None:
        """Compile the model using AdamW and sparse categorical cross-entropy."""
        # Use the optimizer and loss configuration recommended for autoregressive language-model training.
        optimizer = AdamW(
            learning_rate=self.train_cfg["learning_rate"],
            weight_decay=self.train_cfg.get("weight_decay", 0.01),
        )

        model.compile(
            optimizer=optimizer,
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=["accuracy"],
        )

        logger.info("Model compiled (AdamW + SparseCategoricalCrossentropy)")

    def get_callbacks(self) -> list[Callback]:
        """Return the configured fit-time callbacks."""
        # The callback stack handles early-stopping, learning-rate decay, checkpoint saving, and TensorBoard tracking.
        return [
            EarlyStopping(
                monitor="val_loss",
                patience=self.train_cfg["early_stopping_patience"],
                restore_best_weights=True,
                verbose=1,
            ),
            ReduceLROnPlateau(
                monitor="val_loss",
                factor=self.train_cfg["reduce_lr_factor"],
                patience=self.train_cfg["reduce_lr_patience"],
                min_lr=self.train_cfg["min_lr"],
                verbose=1,
            ),
            ModelCheckpoint(
                filepath=str(self.checkpoint_dir / "best_model.keras"),
                monitor="val_loss",
                save_best_only=True,
                verbose=1,
            ),
            TensorBoard(log_dir=str(self.log_dir), histogram_freq=1),
        ]

    def train(
        self,
        model: TransformerCausal,
        train_dataset: tf.data.Dataset,
        validation_dataset: tf.data.Dataset,
    ) -> Any:
        """Execute the fit loop and return the Keras history object."""
        try:
            # Build the callback pipeline before launching the training loop.
            callbacks = self.get_callbacks()
            logger.info("Starting training for up to %d epochs", self.train_cfg["epochs"])

            # Fit the model on the prepared dataset and keep the history object for later report generation.
            history = model.fit(
                train_dataset,
                validation_data=validation_dataset,
                epochs=self.train_cfg["epochs"],
                callbacks=callbacks,
                verbose="auto",
            )

            logger.info("Training finished")
            return history

        except (ValueError, OSError) as exc:
            logger.exception("Training failed during model.fit: %s", exc)
            raise
        except Exception as exc:  # pragma: no cover - guardrail for unexpected Keras failures.
            logger.exception("Unexpected training failure: %s", exc)
            raise
