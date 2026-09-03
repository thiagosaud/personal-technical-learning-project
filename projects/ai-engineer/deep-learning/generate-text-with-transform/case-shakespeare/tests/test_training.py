from pathlib import Path
from unittest.mock import Mock

import tensorflow as tf

from src.core.training.model_trainer import ModelTrainer


def training_config(tmp_path: Path) -> dict:
    return {
        "model": {
            "embed_dim": 8,
            "num_heads": 2,
            "ff_dim": 16,
            "num_layers": 1,
            "dropout_rate": 0,
        },
        "data": {"seq_length": 4},
        "training": {
            "checkpoint_dir": str(tmp_path / "checkpoints"),
            "log_dir": str(tmp_path / "logs"),
            "learning_rate": 0.001,
            "weight_decay": 0.01,
            "epochs": 1,
            "early_stopping_patience": 2,
            "reduce_lr_patience": 1,
            "reduce_lr_factor": 0.5,
            "min_lr": 0.000001,
        },
    }


def test_trainer_creates_artifact_directories_and_model(tmp_path: Path) -> None:
    trainer = ModelTrainer(training_config(tmp_path))

    model = trainer.build_model(vocab_size=10)

    assert trainer.checkpoint_dir.is_dir()
    assert trainer.log_dir.is_dir()
    assert tuple(model(tf.ones((1, 4), dtype=tf.int32)).shape) == (1, 4, 10)


def test_compile_model_sets_optimizer_and_loss(tmp_path: Path) -> None:
    trainer = ModelTrainer(training_config(tmp_path))
    model = trainer.build_model(vocab_size=10)

    trainer.compile_model(model)

    assert model.optimizer is not None
    assert model.loss is not None


def test_get_callbacks_contains_checkpoint_and_tensorboard(tmp_path: Path) -> None:
    trainer = ModelTrainer(training_config(tmp_path))

    callbacks = trainer.get_callbacks()
    callback_names = {type(callback).__name__ for callback in callbacks}

    assert {"EarlyStopping", "ReduceLROnPlateau", "ModelCheckpoint", "TensorBoard"} <= callback_names


def test_train_delegates_to_model_fit(tmp_path: Path) -> None:
    trainer = ModelTrainer(training_config(tmp_path))
    model = Mock()
    expected_history = object()
    model.fit.return_value = expected_history

    result = trainer.train(model, Mock(spec=tf.data.Dataset), Mock(spec=tf.data.Dataset))

    assert result is expected_history
    model.fit.assert_called_once()
