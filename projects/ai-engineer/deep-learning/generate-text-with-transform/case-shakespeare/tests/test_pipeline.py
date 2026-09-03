from pathlib import Path
from unittest.mock import Mock, patch

from src.app.pipeline import Pipeline


def test_pipeline_loads_model_and_vectorizer_once(tmp_path: Path) -> None:
    pipeline = Pipeline.__new__(Pipeline)
    pipeline.model = None
    pipeline.vectorizer = None
    pipeline.config = Mock(data={"seq_length": 4})
    pipeline.config.get_path.side_effect = lambda section, key: {
        ("training", "checkpoint_dir"): tmp_path / "checkpoints",
        ("data", "processed_dir"): tmp_path / "processed",
    }[(section, key)]
    pipeline.logger = Mock()
    model_path = tmp_path / "checkpoints" / "best_model.keras"
    model_path.parent.mkdir()
    model_path.write_bytes(b"model")
    vocabulary_path = tmp_path / "processed" / "vocabulary.txt"
    vocabulary_path.parent.mkdir()
    vocabulary_path.write_text("\n[UNK]\nhello\n", encoding="utf-8")

    loaded_model = Mock()
    with patch("src.app.pipeline.tf.keras.models.load_model", return_value=loaded_model):
        pipeline._load_model_and_vectorizer()

    assert pipeline.model is loaded_model
    assert pipeline.vectorizer is not None
    pipeline.vectorizer(["hello"])


def test_pipeline_plot_generation_skips_when_history_is_missing() -> None:
    pipeline = Pipeline.__new__(Pipeline)
    pipeline.history = None
    pipeline.logger = Mock()

    pipeline._generate_training_plots()

    pipeline.logger.warning.assert_called_once()


def test_pipeline_generate_uses_explicit_arguments() -> None:
    pipeline = Pipeline.__new__(Pipeline)
    pipeline.model = Mock()
    pipeline.vectorizer = Mock()
    pipeline.config = Mock(
        data={"seq_length": 4},
        generation={
            "default_prompt": "default",
            "num_tokens": 10,
            "temperature": 0.7,
            "top_k": 30,
        },
    )
    pipeline.logger = Mock()

    with patch("src.app.pipeline.TextGenerator") as generator_class:
        generator_class.return_value.generate.return_value = "result"
        result = pipeline.generate(prompt="explicit", num_tokens=2, temperature=0.5, top_k=3)

    assert result == "result"
    generator_class.return_value.generate.assert_called_once_with(
        start_string="explicit", num_generate=2, temperature=0.5, top_k=3
    )
