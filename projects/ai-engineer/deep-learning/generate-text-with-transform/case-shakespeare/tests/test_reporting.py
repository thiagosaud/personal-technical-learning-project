from pathlib import Path
from unittest.mock import Mock

import matplotlib
import pytest

from src.core.reporting.generation_reporter import GenerationReporter
from src.core.reporting.history_plotter import HistoryPlotter
from src.core.reporting.model_summary import ModelSummary

matplotlib.use("Agg")


def test_generation_reporter_writes_comparison_report(tmp_path: Path) -> None:
    generator = Mock()
    generator.generate.side_effect = ["sample one", "sample two"]
    reporter = GenerationReporter(generator, output_dir=tmp_path)

    report_path = reporter.generate_report("prompt", temperatures=[0.5, 0.9], num_tokens=2, top_k=3)
    content = report_path.read_text(encoding="utf-8")

    assert report_path.exists()
    assert "Temperature = 0.5" in content
    assert "sample two" in content
    assert generator.generate.call_count == 2


def test_generation_reporter_rejects_invalid_inputs(tmp_path: Path) -> None:
    reporter = GenerationReporter(Mock(), output_dir=tmp_path)

    with pytest.raises(ValueError, match="Prompt cannot"):
        reporter.generate_report(" ")
    with pytest.raises(ValueError, match="cannot be negative"):
        reporter.generate_report("prompt", num_tokens=-1)


def test_history_plotter_accepts_dict_and_writes_figures(tmp_path: Path) -> None:
    plotter = HistoryPlotter(
        {"loss": [2.0, 1.0], "val_loss": [2.5, 1.5], "accuracy": [0.2, 0.4], "val_accuracy": [0.1, 0.3]},
        output_dir=tmp_path,
    )

    plotter.plot_all()

    assert (tmp_path / "loss_curve.png").stat().st_size > 0
    assert (tmp_path / "accuracy_curve.png").stat().st_size > 0


def test_history_plotter_rejects_missing_loss(tmp_path: Path) -> None:
    plotter = HistoryPlotter({"accuracy": [0.2]}, output_dir=tmp_path)

    with pytest.raises(KeyError, match="loss"):
        plotter.plot_loss()


def test_model_summary_uses_disk_size_when_model_file_exists(tmp_path: Path) -> None:
    model = Mock()
    model.count_params.return_value = 100
    model.trainable_weights = []
    model_path = tmp_path / "model.keras"
    model_path.write_bytes(b"1234")
    summary = ModelSummary(model)

    assert summary.total_params == 100
    assert summary.trainable_params == 0
    assert summary.size_in_mb(model_path) == 4 / (1024 * 1024)
