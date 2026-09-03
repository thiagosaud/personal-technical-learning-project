"""High-level orchestration for the Shakespeare CLI workflow."""

from pathlib import Path
from typing import Any

import tensorflow as tf
from keras.layers import TextVectorization
from rich.console import Console

from src.app.logger import Logger
from src.core.config import ProjectConfig
from src.core.data_loader import TextLoader
from src.core.dataset_builder import DatasetBuilder
from src.core.generation.text_generator import TextGenerator
from src.core.model.transformer_causal import TransformerCausal
from src.core.reporting.generation_reporter import GenerationReporter
from src.core.reporting.history_plotter import HistoryPlotter
from src.core.reporting.model_summary import ModelSummary
from src.core.training.model_trainer import ModelTrainer

console = Console()


class Pipeline:
    """Coordinate training, generation, and reporting for the Shakespeare model."""

    def __init__(self, config_path: str | Path = "src/configs/default.yaml") -> None:
        """Load project configuration and prepare the pipeline logger."""
        # Resolve the working config once and retain the runtime logger for the full lifecycle of the pipeline.
        self.config = ProjectConfig(config_path)
        self.logger = Logger().get_logger(name="app.pipeline", level=self.config.project.get("log_level", "INFO"))
        self.model: TransformerCausal | None = None
        self.vectorizer: TextVectorization | None = None
        self.history: Any | None = None

    def _checkpoint_dir(self) -> Path:
        """Return the directory dedicated to saved model artifacts."""
        # All finalized checkpoints live under the outputs folder so the source tree stays clean.
        return self.config.get_path("training", "checkpoint_dir")

    def _processed_vocab_path(self) -> Path:
        """Return the path used to persist the trained vocabulary."""
        # Persist the vocabulary beside the processed data so generation can reproduce the tokenization exactly.
        return self.config.get_path("data", "processed_dir") / "vocabulary.txt"

    def train(self, interactive: bool = False) -> None:
        """Execute the full training workflow."""
        try:
            if interactive:
                # Display the active config before the user decides whether to override it.
                self.config.display()
                answer = console.input("\nDo you want to change any parameter? [y/N]: ").strip().lower()

                # If the user chooses to override, enter an interactive mode to update parameters.
                if answer == "y":
                    self.config.interactive_override()

            # Set the random seed for reproducibility before any TensorFlow operations.
            seed = self.config.project["seed"]
            tf.keras.utils.set_random_seed(seed)
            self.logger.info("Random seed set to %d", seed)

            # Load the corpus and convert it to a training dataset.
            text = TextLoader(self.config.data["raw_path"]).load()
            builder = DatasetBuilder(
                vocab_size=self.config.data["vocab_size"],
                seq_length=self.config.data["seq_length"],
                batch_size=self.config.data["batch_size"],
                buffer_size=self.config.data["buffer_size"],
                validation_split=self.config.data["validation_split"],
            )

            # Prepare the vectorizer and create the training and validation datasets.
            self.vectorizer = builder.prepare_vectorizer(text)
            train_dataset, validation_dataset = builder.create_datasets(text, self.vectorizer)

            # Save the vocabulary so generation can reload the exact tokenizer state later.
            vocab_path = self._processed_vocab_path()
            vocab_path.parent.mkdir(parents=True, exist_ok=True)
            vocab_path.write_text("\n".join(self.vectorizer.get_vocabulary()), encoding="utf-8")

            # Build, compile, and train the model using the prepared datasets.
            trainer = ModelTrainer(self.config.to_dict())
            self.model = trainer.build_model(vocab_size=self.config.data["vocab_size"])
            trainer.compile_model(self.model)

            # Display the model summary before training begins, then start the training loop.
            ModelSummary(self.model).display()
            self.history = trainer.train(self.model, train_dataset, validation_dataset)

            # Save the final model and generate training plots for analysis.
            final_model_path = self._checkpoint_dir() / "final_model.keras"
            final_model_path.parent.mkdir(parents=True, exist_ok=True)
            self.model.save(final_model_path)
            self.logger.info("Model saved to %s", final_model_path)

            # Generate training plots to visualize loss and accuracy trends over epochs.
            self._generate_training_plots()
            ModelSummary(self.model).display(model_path=final_model_path)

        # Handle exceptions gracefully and log them for debugging.
        except (ValueError, OSError) as exc:
            self.logger.exception("Training pipeline failed before completion: %s", exc)
            raise
        except Exception as exc:  # pragma: no cover - safeguard for unexpected runtime problems.
            self.logger.exception("Unexpected error during training: %s", exc)
            raise

    def _generate_training_plots(self) -> None:
        """Persist training curves when history is available."""
        # Keep training figures separate from source code by writing them to the project outputs directory.
        figures_dir = Path("outputs/reports/figures").resolve()
        figures_dir.mkdir(parents=True, exist_ok=True)

        # If no training history is available, log a warning and skip plot generation.
        if self.history is None:
            self.logger.warning(
                "No training history available; skipping plot generation. Directory ready at %s", figures_dir
            )

            return

        try:
            # Generate and save loss and accuracy plots using the training history.
            plotter = HistoryPlotter(self.history)
            plotter.plot_all()

        # Handle exceptions during plotting but do not interrupt the main training workflow.
        except Exception as exc:
            self.logger.exception("Failed to save training plots: %s", exc)

    def _load_model_and_vectorizer(self, model_path: str | None = None) -> None:
        """Load the trained model and its persisted vocabulary lazily."""

        # If the model and vectorizer are already loaded, skip reloading to save time.
        if self.model is not None and self.vectorizer is not None:
            return

        try:
            # If a specific model path is provided, add it to the list of candidates for loading.
            candidate_paths: list[Path] = []
            if model_path is not None:
                candidate_paths.append(Path(model_path))

            # If no specific model path is provided, check the default checkpoint directory for saved models.
            candidate_paths.extend(
                [
                    self._checkpoint_dir() / "best_model.keras",
                    self._checkpoint_dir() / "final_model.keras",
                ]
            )

            # Resolve the first existing model path from the list of candidates; raise an error if none are found.
            resolved_model_path = next((path for path in candidate_paths if path.exists()), None)
            if resolved_model_path is None:
                raise FileNotFoundError(
                    f"No trained model found in {self._checkpoint_dir()}. Please run training first."
                )

            # Load the model from the resolved path, ensuring that the custom TransformerCausal class is recognized.
            self.logger.info("Loading model from %s", resolved_model_path)
            self.model = tf.keras.models.load_model(
                resolved_model_path,
                custom_objects={"TransformerCausal": TransformerCausal},
            )

            # Load the persisted vocabulary from the processed directory and initialize the TextVectorization layer.
            vocabulary = self._processed_vocab_path().read_text(encoding="utf-8").splitlines()
            if not vocabulary:
                raise ValueError(f"Vocabulary file is empty: {self._processed_vocab_path()}")

            # Initialize the TextVectorization layer with the loaded vocabulary and configuration parameters.
            self.vectorizer = TextVectorization(
                max_tokens=len(vocabulary),
                output_mode="int",
                standardize="lower_and_strip_punctuation",
                output_sequence_length=self.config.data["seq_length"],
            )

            self.vectorizer.set_vocabulary(vocabulary)

        # Handle exceptions during model or vocabulary loading and log them for debugging.
        except (ValueError, OSError) as exc:
            self.logger.exception("Failed to load model or vocabulary: %s", exc)
            raise

    def generate(
        self,
        prompt: str | None = None,
        num_tokens: int | None = None,
        temperature: float | None = None,
        top_k: int | None = None,
        interactive: bool = False,
    ) -> str:
        """Generate text from an optional prompt and sampling configuration."""
        try:
            # If interactive mode is enabled, display the current configuration and allow the user to override params.
            if interactive:
                self.config.display(title="Generation Configuration")

                # Prompt the user to decide whether to override any generation parameters interactively.
                answer = console.input("\nDo you want to change any generation parameter? [y/N]: ").strip().lower()
                if answer == "y":
                    self.config.interactive_override()

            # Load the trained model and vectorizer, ensuring they are available for text generation.
            self._load_model_and_vectorizer()

            # Retrieve the generation configuration from the project config for default values.
            generation_config = self.config.generation

            # Keep explicit runtime arguments higher priority than YAML defaults.
            resolved_prompt = prompt if prompt is not None else generation_config["default_prompt"]
            resolved_tokens = num_tokens if num_tokens is not None else generation_config["num_tokens"]
            resolved_temperature = temperature if temperature is not None else generation_config["temperature"]
            resolved_top_k = top_k if top_k is not None else generation_config["top_k"]

            # Validate the resolved parameters to ensure they are suitable for generation.
            generator = TextGenerator(
                model=self.model,
                vectorizer=self.vectorizer,
                seq_length=self.config.data["seq_length"],
            )

            # Log the resolved generation parameters for traceability and debugging purposes.
            self.logger.info(
                "Generating %d tokens | temperature=%.2f | top_k=%d",
                resolved_tokens,
                resolved_temperature,
                resolved_top_k,
            )

            # Handle exceptions during generation setup and log them for debugging.
            result = generator.generate(
                start_string=resolved_prompt,
                num_generate=resolved_tokens,
                temperature=resolved_temperature,
                top_k=resolved_top_k,
            )

            console.print("\n" + "=" * 80)
            console.print(result)
            console.print("=" * 80 + "\n")
            return result

        # Handle exceptions during generation and log them for debugging.
        except (FileNotFoundError, ValueError) as exc:
            self.logger.exception("Generation failed due to missing resources or invalid values: %s", exc)
            raise
        except Exception as exc:  # pragma: no cover - unexpected generation failure guard.
            self.logger.exception("Unexpected generation failure: %s", exc)
            raise

    def create_generation_report(
        self,
        prompt: str | None = None,
        temperatures: list[float] | None = None,
    ) -> Path:
        """Write a generation report comparing multiple temperatures."""
        try:
            # Load the trained model and vectorizer to ensure they are available for generating text for the report.
            self._load_model_and_vectorizer()

            # If no specific temperatures are provided, use a default set for the report.
            generator = TextGenerator(
                model=self.model,
                vectorizer=self.vectorizer,
                seq_length=self.config.data["seq_length"],
            )

            # Create a GenerationReporter instance to handle the report generation and saving.
            reporter = GenerationReporter(generator)

            # Resolve the prompt to use for the report, falling back to the default if none is provided.
            resolved_prompt = prompt if prompt is not None else self.config.generation["default_prompt"]
            report_path = reporter.generate_report(
                prompt=resolved_prompt,
                temperatures=temperatures,
                num_tokens=self.config.generation["num_tokens"],
                top_k=self.config.generation["top_k"],
            )

            self.logger.info("Generation report saved to %s", report_path)
            return report_path

        # Handle exceptions during report generation and log them for debugging.
        except Exception as exc:
            self.logger.exception("Failed to create generation report: %s", exc)
            raise
