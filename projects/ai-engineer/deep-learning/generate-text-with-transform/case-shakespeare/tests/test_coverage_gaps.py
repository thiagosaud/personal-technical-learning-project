from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import MagicMock, Mock, patch

import numpy as np
import pytest
import tensorflow as tf
from keras.layers import TextVectorization

from src.app.cli import CLI
from src.app.pipeline import Pipeline
from src.core.config import ProjectConfig
from src.core.data_loader import TextLoader
from src.core.dataset_builder import DatasetBuilder
from src.core.generation.text_generator import TextGenerator
from src.core.reporting.generation_reporter import GenerationReporter
from src.core.reporting.history_plotter import HistoryPlotter
from src.core.reporting.model_summary import ModelSummary
from src.core.training.model_trainer import ModelTrainer


def full_config(tmp_path: Path) -> dict:
    return {
        "project": {"seed": 42, "log_level": "INFO"},
        "data": {
            "raw_path": str(tmp_path / "raw.txt"),
            "processed_dir": str(tmp_path / "processed"),
            "vocab_size": 10,
            "seq_length": 2,
            "batch_size": 1,
            "buffer_size": 2,
            "validation_split": 0.5,
        },
        "model": {"embed_dim": 8, "num_heads": 2, "ff_dim": 16, "num_layers": 1, "dropout_rate": 0},
        "training": {
            "checkpoint_dir": str(tmp_path / "checkpoints"),
            "log_dir": str(tmp_path / "logs"),
            "learning_rate": 0.001,
            "weight_decay": 0.01,
            "epochs": 1,
            "early_stopping_patience": 1,
            "reduce_lr_patience": 1,
            "reduce_lr_factor": 0.5,
            "min_lr": 0.000001,
        },
        "generation": {"default_prompt": "hello", "num_tokens": 2, "temperature": 0.7, "top_k": 2},
    }


def make_pipeline(config: Mock) -> Pipeline:
    pipeline = Pipeline.__new__(Pipeline)
    pipeline.config = config
    pipeline.logger = Mock()
    pipeline.model = Mock()
    pipeline.vectorizer = Mock()
    pipeline.history = None
    return pipeline


def test_config_fallback_and_properties(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    fallback = tmp_path / "src" / "app" / "configs" / "default.yaml"
    fallback.parent.mkdir(parents=True)
    fallback.write_text("project: {}\ndata: {}\nmodel: {}\ntraining: {}\ngeneration: {}\n", encoding="utf-8")
    monkeypatch.setattr(ProjectConfig, "PROJECT_ROOT", tmp_path)

    config = ProjectConfig("missing.yaml")

    assert config.path == fallback
    assert config.model == {}
    assert config.training == {}
    assert config.generation == {}
    assert config.resolve_path("file.txt") == (tmp_path / "file.txt").resolve()


def test_config_raises_when_config_and_fallback_are_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ProjectConfig, "PROJECT_ROOT", tmp_path)
    with pytest.raises(FileNotFoundError, match="Config file not found"):
        ProjectConfig("missing.yaml")


def test_config_display_and_interactive_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "config.yaml"
    path.write_text(
        "project: {seed: 1}\ndata: {vocab_size: 10, seq_length: 4, batch_size: 2}\n"
        "model: {num_layers: 1, embed_dim: 8}\n"
        "training: {epochs: 1, learning_rate: 0.1}\n"
        "generation: {default_prompt: hi, num_tokens: 2, temperature: 0.7, top_k: 2}\n",
        encoding="utf-8",
    )
    config = ProjectConfig(path)
    inputs = iter(["11", "", "bad", "2", "16", "3", "0.01", "new", "4", "0.8", "5"])
    monkeypatch.setattr("src.core.config.console.input", lambda _: next(inputs))
    monkeypatch.setattr("src.core.config.console.print", Mock())

    config.display()
    config.interactive_override()

    assert config.data["vocab_size"] == 11
    assert config.data["batch_size"] == 2
    assert config.model["num_layers"] == 2
    assert config.model["embed_dim"] == 16
    assert config.training["epochs"] == 3
    assert config.training["learning_rate"] == 0.01
    assert config.generation["default_prompt"] == "new"
    assert config.generation["num_tokens"] == 4
    assert config.generation["temperature"] == 0.8
    assert config.generation["top_k"] == 5


def test_text_loader_wraps_read_errors(tmp_path: Path) -> None:
    path = tmp_path / "corpus.txt"
    path.write_text("text", encoding="utf-8")
    loader = TextLoader(path)
    with patch.object(Path, "read_text", side_effect=OSError("denied")):  # noqa: SIM117
        with pytest.raises(RuntimeError, match="Unable to read"):
            loader.load()


def test_dataset_builder_handles_empty_batches_and_validation_split() -> None:
    builder = DatasetBuilder(vocab_size=10, seq_length=2, batch_size=1)
    with pytest.raises(ValueError, match="empty"):
        builder._make_dataset(np.array([]), np.array([]))
    dataset = builder._make_dataset(np.array([[1, 2]]), np.array([[2, 3]]))
    assert next(iter(dataset))[0].shape == (1, 2)


def test_dataset_builder_creates_datasets_with_non_default_split() -> None:
    builder = DatasetBuilder(vocab_size=10, seq_length=2, batch_size=1, validation_split=0.25)
    vectorizer = TextVectorization(max_tokens=10, output_mode="int")
    vectorizer.adapt(["one two three four five six seven eight"])

    train_dataset, validation_dataset = builder.create_datasets("one two three four five six seven eight", vectorizer)

    assert train_dataset is not None
    assert validation_dataset is not None


def test_dataset_builder_prepares_vectorizer_for_valid_text() -> None:
    builder = DatasetBuilder(vocab_size=10, seq_length=2, batch_size=1)

    vectorizer = builder.prepare_vectorizer("one two three")

    assert "one" in vectorizer.get_vocabulary()


def test_generator_covers_top_k_and_unknown_generated_token() -> None:
    generator = TextGenerator.__new__(TextGenerator)
    generator.model = Mock(return_value=tf.constant([[[0.0, 0.0, 0.0, 0.0]]]))
    generator.vectorizer = MagicMock()
    vectorized = MagicMock()
    vectorized.__getitem__.return_value.numpy.return_value = np.array([1], dtype=np.int32)
    generator.vectorizer.return_value = vectorized
    generator.seq_length = 2
    generator.vocabulary = ["", "[UNK]", "known"]

    logits = tf.constant([[1.0, 2.0, 3.0, 4.0]])
    filtered = generator._top_k_filtering(logits, 2)
    assert int(tf.math.count_nonzero(filtered < -1e8)) == 2

    with patch("src.core.generation.text_generator.tf.random.categorical", return_value=tf.constant([[3]])):
        result = generator.generate("prompt", num_generate=1, top_k=2)
    assert result == "prompt "


def test_reporter_uses_default_temperatures(tmp_path: Path) -> None:
    generator = Mock()
    generator.generate.return_value = "sample"
    report = GenerationReporter(generator, tmp_path).generate_report("prompt", num_tokens=0)

    assert report.exists()
    assert generator.generate.call_count == 4


def test_history_plotter_accepts_history_object_and_accuracy_without_series(tmp_path: Path) -> None:
    history = SimpleNamespace(history={"loss": [1.0]})
    plotter = HistoryPlotter(history, tmp_path)
    with patch("matplotlib.axes.Axes.legend"):
        plotter.plot_accuracy()
    assert (tmp_path / "accuracy_curve.png").exists()
    with pytest.raises(TypeError, match="requires"):
        HistoryPlotter(42, tmp_path)


def test_model_summary_estimates_size_and_displays() -> None:
    model = Mock()
    model.count_params.return_value = 1024
    model.trainable_weights = []
    summary = ModelSummary(model)

    assert summary.size_in_mb() == 4096 / (1024 * 1024)
    with patch("src.core.reporting.model_summary.console.print") as printer:
        summary.display()
    printer.assert_called_once()


def test_trainer_resolves_absolute_paths_and_logs_model_summary(tmp_path: Path) -> None:
    trainer = ModelTrainer({**full_config(tmp_path), "training": full_config(tmp_path)["training"]})
    assert trainer._resolve_path(tmp_path / "absolute") == tmp_path / "absolute"
    assert trainer.build_model(10).count_params() > 0


def test_trainer_wraps_fit_errors(tmp_path: Path) -> None:
    trainer = ModelTrainer(full_config(tmp_path))
    model = Mock()
    model.fit.side_effect = ValueError("invalid fit")
    train_dataset = Mock()
    validation_dataset = Mock()

    with pytest.raises(ValueError, match="invalid fit"):
        trainer.train(model, train_dataset, validation_dataset)


def test_pipeline_load_errors_and_report_flow(tmp_path: Path) -> None:
    config = Mock()
    config.data = {"seq_length": 2}
    config.generation = {"default_prompt": "default", "num_tokens": 2, "top_k": 2}
    config.get_path.return_value = tmp_path / "missing"
    pipeline = make_pipeline(config)
    pipeline.model = None
    pipeline.vectorizer = None

    with pytest.raises(FileNotFoundError, match="No trained model"):
        pipeline._load_model_and_vectorizer()

    pipeline = make_pipeline(config)
    with (
        patch.object(pipeline, "_load_model_and_vectorizer"),
        patch("src.app.pipeline.TextGenerator") as generator_class,
    ):
        generator_class.return_value.generate_report = Mock(return_value=tmp_path / "report.md")
        with patch("src.app.pipeline.GenerationReporter") as reporter_class:
            reporter_class.return_value.generate_report.return_value = tmp_path / "report.md"
            result = pipeline.create_generation_report()

    assert result == tmp_path / "report.md"
    reporter_class.return_value.generate_report.assert_called_once()


def test_pipeline_rejects_empty_vocabulary_and_handles_cached_resources(tmp_path: Path) -> None:
    config = Mock()
    config.data = {"seq_length": 2}
    config.get_path.side_effect = lambda section, key: {
        ("training", "checkpoint_dir"): tmp_path / "checkpoints",
        ("data", "processed_dir"): tmp_path / "processed",
    }[(section, key)]
    checkpoint = tmp_path / "checkpoints" / "best_model.keras"
    checkpoint.parent.mkdir()
    checkpoint.write_bytes(b"model")
    vocabulary = tmp_path / "processed" / "vocabulary.txt"
    vocabulary.parent.mkdir()
    vocabulary.write_text("", encoding="utf-8")
    pipeline = make_pipeline(config)
    pipeline.model = None
    pipeline.vectorizer = None

    with patch("src.app.pipeline.tf.keras.models.load_model", return_value=Mock()):  # noqa: SIM117
        with pytest.raises(ValueError, match="empty"):
            pipeline._load_model_and_vectorizer()

    cached = make_pipeline(config)
    cached._load_model_and_vectorizer = Mock()
    cached.model = Mock()
    cached.vectorizer = Mock()
    Pipeline._load_model_and_vectorizer(cached)
    assert cached.model is not None


def test_pipeline_training_orchestrates_artifacts(tmp_path: Path) -> None:
    config_data = full_config(tmp_path)
    config = Mock()
    config.project = config_data["project"]
    config.data = config_data["data"]
    config.to_dict.return_value = config_data
    config.get_path.side_effect = lambda section, key: {
        ("training", "checkpoint_dir"): tmp_path / "checkpoints",
        ("data", "processed_dir"): tmp_path / "processed",
    }[(section, key)]
    pipeline = Pipeline.__new__(Pipeline)
    pipeline.config = config
    pipeline.logger = Mock()
    pipeline.model = None
    pipeline.vectorizer = None
    pipeline.history = None
    (tmp_path / "raw.txt").write_text("one two three four five", encoding="utf-8")
    trainer = Mock()
    trainer.build_model.return_value = Mock()
    trainer.train.return_value = {"loss": [1.0]}

    with (
        patch("src.app.pipeline.ModelTrainer", return_value=trainer),
        patch("src.app.pipeline.DatasetBuilder") as builder_class,
        patch("src.app.pipeline.ModelSummary"),
        patch("src.app.pipeline.HistoryPlotter"),
    ):
        vectorizer = Mock()
        vectorizer.get_vocabulary.return_value = ["", "one"]
        builder_class.return_value.prepare_vectorizer.return_value = vectorizer
        builder_class.return_value.create_datasets.return_value = (Mock(), Mock())
        pipeline.train()

    assert pipeline.model is trainer.build_model.return_value
    assert (tmp_path / "processed" / "vocabulary.txt").exists()
    trainer.build_model.return_value.save.assert_called_once()


def test_pipeline_training_interactive_mode_keeps_configuration(tmp_path: Path) -> None:
    config_data = full_config(tmp_path)
    config = Mock()
    config.project = config_data["project"]
    config.data = config_data["data"]
    config.to_dict.return_value = config_data
    config.get_path.side_effect = lambda section, key: {
        ("training", "checkpoint_dir"): tmp_path / "checkpoints",
        ("data", "processed_dir"): tmp_path / "processed",
    }[(section, key)]
    pipeline = Pipeline.__new__(Pipeline)
    pipeline.config = config
    pipeline.logger = Mock()
    pipeline.model = None
    pipeline.vectorizer = None
    pipeline.history = None
    (tmp_path / "raw.txt").write_text("one two three four five", encoding="utf-8")
    trainer = Mock()
    trainer.build_model.return_value = Mock()
    trainer.train.return_value = {"loss": [1.0]}

    with (
        patch("src.app.pipeline.console.input", return_value="n"),
        patch("src.app.pipeline.ModelTrainer", return_value=trainer),
        patch("src.app.pipeline.DatasetBuilder") as builder_class,
        patch("src.app.pipeline.ModelSummary"),
        patch("src.app.pipeline.HistoryPlotter"),
    ):
        vectorizer = Mock()
        vectorizer.get_vocabulary.return_value = ["", "one"]
        builder_class.return_value.prepare_vectorizer.return_value = vectorizer
        builder_class.return_value.create_datasets.return_value = (Mock(), Mock())
        pipeline.train(interactive=True)

    config.display.assert_called_once()


def test_pipeline_training_interactive_override_and_value_error(tmp_path: Path) -> None:
    config_data = full_config(tmp_path)
    config = Mock()
    config.project = config_data["project"]
    config.data = config_data["data"]
    config.to_dict.return_value = config_data
    config.get_path.side_effect = lambda section, key: {
        ("training", "checkpoint_dir"): tmp_path / "checkpoints",
        ("data", "processed_dir"): tmp_path / "processed",
    }[(section, key)]
    pipeline = Pipeline.__new__(Pipeline)
    pipeline.config = config
    pipeline.logger = Mock()
    pipeline.model = None
    pipeline.vectorizer = None
    pipeline.history = None
    config.display = Mock()
    config.interactive_override = Mock()
    with (  # noqa: SIM117
        patch("src.app.pipeline.console.input", return_value="y"),
        patch.object(config, "interactive_override", config.interactive_override),
        patch("src.app.pipeline.TextLoader", side_effect=ValueError("bad data")),
    ):
        with pytest.raises(ValueError, match="bad data"):
            pipeline.train(interactive=True)
    config.interactive_override.assert_called_once()


def test_pipeline_generate_and_report_error_paths() -> None:
    pipeline = make_pipeline(Mock())
    pipeline._load_model_and_vectorizer = Mock(side_effect=FileNotFoundError("missing"))
    with pytest.raises(FileNotFoundError):
        pipeline.generate()

    pipeline._load_model_and_vectorizer = Mock()
    config_mock = cast(Any, pipeline.config)
    config_mock.configure_mock(
        data={"seq_length": 2},
        generation={"default_prompt": "x", "num_tokens": 1, "temperature": 0.7, "top_k": 2},
    )
    with patch("src.app.pipeline.TextGenerator", side_effect=RuntimeError("generation failed")):  # noqa: SIM117
        with pytest.raises(RuntimeError):
            pipeline.generate()

    with patch("src.app.pipeline.TextGenerator", side_effect=RuntimeError("report failed")):  # noqa: SIM117
        with pytest.raises(RuntimeError):
            pipeline.create_generation_report()


def test_pipeline_generate_interactive_override_and_explicit_model_path(tmp_path: Path) -> None:
    config = Mock()
    config.data = {"seq_length": 2}
    config.generation = {"default_prompt": "x", "num_tokens": 1, "temperature": 0.7, "top_k": 2}
    config.get_path.side_effect = lambda _section, key: tmp_path / key
    model_path = tmp_path / "custom.keras"
    model_path.write_bytes(b"model")
    vocabulary_path = tmp_path / "processed_dir" / "vocabulary.txt"
    vocabulary_path.parent.mkdir()
    vocabulary_path.write_text("\n[UNK]\nhello\n", encoding="utf-8")
    pipeline = make_pipeline(config)
    pipeline.model = None
    pipeline.vectorizer = None
    with patch("src.app.pipeline.tf.keras.models.load_model", return_value=Mock()):
        pipeline._load_model_and_vectorizer(model_path=str(model_path))
    assert pipeline.vectorizer is not None

    pipeline = make_pipeline(config)
    pipeline.config.interactive_override = Mock()
    pipeline._load_model_and_vectorizer = Mock()
    with (
        patch("src.app.pipeline.console.input", return_value="y"),
        patch("src.app.pipeline.TextGenerator") as generator_class,
    ):
        generator_class.return_value.generate.return_value = "result"
        assert pipeline.generate(interactive=True) == "result"
    pipeline.config.interactive_override.assert_called_once()


def test_pipeline_plot_errors_are_logged() -> None:
    pipeline = Pipeline.__new__(Pipeline)
    pipeline.history = {"loss": [1.0]}
    pipeline.logger = Mock()
    with patch("src.app.pipeline.HistoryPlotter", side_effect=RuntimeError("plot failed")):
        pipeline._generate_training_plots()
    pipeline.logger.exception.assert_called_once()


def test_cli_dispatches_train_and_generate_and_handles_value_error() -> None:
    pipeline = Mock()
    with patch("sys.argv", ["cli", "train"]), patch("src.app.cli.Pipeline", return_value=pipeline):
        CLI().run()
    pipeline.train.assert_called_once_with(interactive=False)

    with patch("sys.argv", ["cli", "generate", "--tokens", "3"]), patch("src.app.cli.Pipeline", return_value=pipeline):
        CLI().run()
    pipeline.generate.assert_called_once()

    with patch("sys.argv", ["cli", "generate"]), patch("src.app.cli.Pipeline", side_effect=ValueError("bad")):
        cli = CLI()
        with pytest.raises(SystemExit) as error:
            cli.run()
    assert error.value.code == 1


def test_cli_handles_unexpected_errors_and_unknown_command() -> None:
    cli = CLI()
    cli.parser.parse_args = Mock(return_value=SimpleNamespace(command="unknown", config="config"))
    cli.parser.print_help = Mock()
    with patch("src.app.cli.Pipeline"):
        cli.run()
    cli.parser.print_help.assert_called_once()

    cli.parser.parse_args = Mock(side_effect=RuntimeError("unexpected"))
    with pytest.raises(SystemExit) as error:
        cli.run()
    assert error.value.code == 1


def test_direct_entrypoints_invoke_their_main_functions() -> None:
    import runpy

    cli_path = Path(__file__).parents[1] / "src" / "app" / "cli.py"
    with patch("sys.argv", ["case-shakespeare", "--help"]), pytest.raises(SystemExit):
        runpy.run_path(str(cli_path), run_name="__main__")

    main_path = Path(__file__).parents[1] / "src" / "main.py"
    with patch("sys.argv", ["case-shakespeare", "generate"]), patch("src.app.cli.CLI.run") as cli_run:
        runpy.run_path(str(main_path), run_name="__main__")
    cli_run.assert_called_once()


def test_gradio_interface_callback_forwards_inputs() -> None:
    from src.app.infrastructure.gradio_app import create_interface

    pipeline = Mock()
    pipeline.generate.return_value = "generated"
    with patch("src.app.infrastructure.gradio_app.Pipeline", return_value=pipeline):
        interface = create_interface()

    assert interface.fn("prompt", 0.7, 20, 50) == "generated"
    pipeline.generate.assert_called_once_with(
        prompt="prompt", temperature=0.7, top_k=20, num_tokens=50, interactive=False
    )


def test_gradio_direct_entrypoint_launches_mocked_app() -> None:
    import runpy

    app = Mock()
    gradio_path = Path(__file__).parents[1] / "src" / "app" / "infrastructure" / "gradio_app.py"
    with (
        patch("sys.argv", ["gradio_app"]),
        patch("src.app.infrastructure.gradio_app.Pipeline"),
        patch("gradio.Interface", return_value=app),
    ):
        runpy.run_path(str(gradio_path), run_name="__main__")
    app.launch.assert_called_once()
