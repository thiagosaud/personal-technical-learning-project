"""Unit tests for ModelTrainerLayer."""

import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression, LogisticRegression

from layer.data.etl import ETLLayer
from layer.machine_learning.model_trainer import ModelTrainerLayer


@pytest.fixture
def processed_data() -> pd.DataFrame:
    """Fixture providing clean processed dataset for training tests."""
    return ETLLayer().run_etl()


def test_model_trainer_execution(processed_data: pd.DataFrame) -> None:
    """Validates training pipeline execution and metric boundary ranges."""
    trainer = ModelTrainerLayer(processed_data)
    scores = trainer.train_models()

    # Checks expected score dictionary keys
    assert "case1_r2" in scores
    assert "case2_r2" in scores
    assert "case3_acc" in scores

    # Validates trained models are instantiated correctly
    assert isinstance(trainer.simple_linear_model, LinearRegression)
    assert isinstance(trainer.multiple_linear_model, LinearRegression)
    assert isinstance(trainer.logistic_model, LogisticRegression)

    # Validates metric constraints (R2 and Accuracy ranges)
    assert 0.0 <= scores["case1_r2"] <= 1.0
    assert 0.0 <= scores["case2_r2"] <= 1.0
    assert 0.0 <= scores["case3_acc"] <= 1.0
