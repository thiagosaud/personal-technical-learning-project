"""Unit tests for ModelVisualizerLayer."""

from pathlib import Path

import pandas as pd
import pytest

from src.layer.data.etl import ETLLayer
from src.layer.machine_learning.model_trainer import ModelTrainerLayer
from src.layer.visualizer.model_visualizer import ModelVisualizerLayer


@pytest.fixture
def trained_pipeline() -> tuple[pd.DataFrame, ModelTrainerLayer]:
    """Fixture providing dataset and trained models ready for visualization."""
    df = ETLLayer().run_etl()
    trainer = ModelTrainerLayer(df)
    trainer.train_models()
    return df, trainer


def test_visualizer_generates_plots(trained_pipeline: tuple[pd.DataFrame, ModelTrainerLayer], tmp_path: Path) -> None:
    """Verifies that all three case plots are successfully rendered and persisted as PNG files."""
    df, trainer = trained_pipeline

    # ==========================================
    # TYPE NARROWING VIA TEST ASSERTIONS
    # ==========================================
    # These native assertions prove to the type checker that the underlying model instances
    # are physically instantiated and not None before passing them down to plotting routines.
    assert trainer.simple_linear_model is not None, "Simple linear model training payload failed to initialize."
    assert trainer.multiple_linear_model is not None, "Multiple linear model training payload failed to initialize."
    assert trainer.logistic_model is not None, "Logistic classification engine payload failed to initialize."

    # Passes tmp_path fixture to isolate generated artifacts during test runs safely
    visualizer = ModelVisualizerLayer(data=df, output_dir=tmp_path)

    # Triggers plot generation methods with guaranteed type-safe initialized inputs
    visualizer.generate_case1_plot(trainer.simple_linear_model, 0.85)
    visualizer.generate_case2_plot(trainer.multiple_linear_model, 0.90)
    visualizer.generate_case3_plot(trainer.logistic_model, 0.95)

    # Asserts files were correctly created in the temporary target directory
    expected_files = [
        "byd_case1_linear_simples.png",
        "byd_case2_linear_multiple.png",
        "byd_case3_logistic.png",
    ]

    for filename in expected_files:
        file_path = tmp_path / filename
        assert file_path.exists(), f"Expected plot artifact {filename} was not generated."
        assert file_path.stat().st_size > 0, f"Plot artifact {filename} is empty."


def test_visualizer_default_output_dir(trained_pipeline: tuple[pd.DataFrame, ModelTrainerLayer]) -> None:
    """Verifies that default output_dir falls back correctly to the case path when not specified."""
    df, _ = trained_pipeline
    visualizer = ModelVisualizerLayer(data=df)

    # Assert that it correctly mapped to the expected dynamic path structure
    assert visualizer.output_dir.name == "figures"
    assert visualizer.output_dir.parent.name == "outputs"
