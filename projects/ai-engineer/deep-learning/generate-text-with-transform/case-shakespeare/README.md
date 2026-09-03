# 🏗️ Shakespeare Deep Learning Case

[![Python](https://img.shields.io/badge/python-%3E%3D3.12-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Keras](https://img.shields.io/badge/Keras-D00000?logo=keras&logoColor=white)](https://keras.io/)
[![Gradio](https://img.shields.io/badge/Gradio-FF7A59?logo=gradio&logoColor=white)](https://www.gradio.app/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../../LICENSE)

Educational deep learning project for generating text in the style of William Shakespeare using a causal Transformer implemented in TensorFlow/Keras.

This project covers the full flow:

1. Raw text preparation and vocabulary creation.
2. Dataset building and tokenization.
3. Transformer model training.
4. Model checkpointing and TensorBoard logging.
5. Text generation with sampling controls.
6. Markdown report generation.
7. Optional local web interface with Gradio.

## ⚠️ Scope

This project is a technical and educational demonstration focused on training a generative language model from a small corpus.

The source text is loaded directly from the project data folder and not from an external database or API.

The model is trained and evaluated on the same corpus in a lab-like setup, so the objective is to demonstrate the workflow and generation behavior, not to build a production-grade language model.

## ⚙️ Requirements

See the project dependencies in [pyproject.toml](pyproject.toml).

The project uses:

- Python >= 3.12
- uv for environment management
- TensorFlow + Keras
- Gradio
- Rich
- PyYAML
- TensorBoard

## ▶️ Setup and execution order

Run the commands in this exact order:

1. Install dependencies
2. Train the model
3. Generate text
4. Create the markdown report
5. Launch the Gradio interface (optional)

Important: the generation and report commands depend on a trained model being present in the checkpoint folder.

### 1) Train the model

```bash
pnpm build:train
```

Equivalent direct command:

```bash
uv run python -m src.main train
```

Available flags:

```bash
uv run python -m src.main train --config <path-to-yaml> --interactive
```

- `--config`: path to the YAML config file.
- `--interactive`: opens the interactive configuration override flow before starting training.

This step creates:

- vocabulary under `outputs/data/processed/vocabulary.txt`
- training logs under `outputs/logs/`
- saved model checkpoints under `outputs/checkpoints/`
- generated training plots under `outputs/reports/figures/`

### 2) Generate text

```bash
pnpm build:generate
```

Equivalent direct command:

```bash
uv run python -m src.main generate --prompt "To be, or not to be"
```

Available flags:

```bash
uv run python -m src.main generate \
  --config <path-to-yaml> \
  --interactive \
  --prompt "Your starting sentence" \
  --tokens 300 \
  --temperature 0.75 \
  --top_k 40
```

- `--config`: YAML file with project settings.
- `--interactive`: interactive generation configuration override.
- `--prompt`: starting text for generation.
- `--tokens`: number of tokens to generate.
- `--temperature`: sampling temperature.
- `--top_k`: restricts sampling to the top-k candidates.

Notes:

- If no prompt is provided, the project uses the default in the config.
- If no values are passed, it uses the defaults defined in `src/app/configs/default.yaml`.

### 3) Generate a markdown report

```bash
pnpm build:report
```

Equivalent direct command:

```bash
uv run python -m src.main report --prompt "To be, or not to be"
```

Available flags:

```bash
uv run python -m src.main report --config <path-to-yaml> --prompt "Your prompt"
```

- `--config`: YAML config path.
- `--prompt`: text used to generate the report comparison.

This command creates a Markdown report under the project report directory and logs the generated file location.

### 4) Launch the Gradio interface (optional)

```bash
pnpm build:with:interface
```

Equivalent direct command:

```bash
uv run python -m src.app.infrastructure.gradio_app
```

This starts the local web UI for interactive generation, with:

- prompt input
- temperature slider
- top-k slider
- number of tokens slider

## 📁 Structure

```text
case-shakespeare/
├── README.md # Project overview, setup instructions, and usage flow
├── CHANGELOG.md # Project changelog and release history
├── pyproject.toml # Python package metadata and dependency declarations
├── package.json # Script shortcuts for training, generation, report generation, and interface launch
├── data/ # Local raw text assets used by the project
│   └── raw/ # Raw corpus inputs
│       └── shakespeare.txt # Shakespeare source text used for training and generation
├── outputs/ # Generated runtime artifacts and project deliverables
│   ├── checkpoints/ # Saved model checkpoints and final trained weights
│   │   ├── best_model.keras # Best validation checkpoint
│   │   └── final_model.keras # Final trained model artifact
│   ├── data/ # Processed runtime data
│   │   └── processed/ # Derived data files created during preprocessing
│   │       └── vocabulary.txt # Tokenizer vocabulary persisted after vectorization
│   ├── logs/ # Training and validation diagnostics
│   │   ├── train/ # TensorBoard logs from the training run
│   │   │   └── events.out.tfevents.* # TensorFlow event files for training metrics
│   │   └── validation/ # Validation-specific TensorBoard event files
│   │       └── events.out.tfevents.* # TensorFlow event files for validation metrics
│   └── reports/ # Generated training and generation artifacts
│       ├── figures/ # PNG charts for loss and accuracy curves
│       │   ├── loss_curve.png # Training/validation loss plot
│       │   └── accuracy_curve.png # Training/validation accuracy plot
│       └── generation/ # Markdown prompt comparison reports
│           └── generation_report_*.md # Temperature-based generation report output
├── src/ # Main application source code
│   ├── main.py # CLI entry point for the project
│   ├── app/ # Application orchestration and entry logic
│   │   ├── cli.py # Command-line handler for train/generate/report commands
│   │   ├── logger.py # Shared logging setup
│   │   ├── pipeline.py # High-level pipeline for training, generation, and reporting
│   │   ├── configs/ # Runtime configuration files
│   │   │   └── default.yaml # Default project configuration and paths
│   │   └── infrastructure/ # User-facing runtime integrations
│   │       └── gradio_app.py # Optional local Gradio interface for generation
│   ├── core/ # Core model, dataset, generation, training, and reporting logic
│   │   ├── config.py # Project configuration access and path resolution helpers
│   │   ├── data_loader.py # Raw corpus reader and loader implementation
│   │   ├── dataset_builder.py # Dataset preparation, tokenization, and batching logic
│   │   ├── generation/ # Text generation logic
│   │   │   └── text_generator.py # Temperature and top-k generation implementation
│   │   ├── model/ # Transformer architecture components
│   │   │   ├── transformer_block.py # Transformer block definition
│   │   │   └── transformer_causal.py # Causal language model implementation
│   │   ├── reporting/ # Reporting and chart creation utilities
│   │   │   ├── generation_reporter.py # Markdown report generator for text sampling comparisons
│   │   │   ├── history_plotter.py # Plot creation for training curves
│   │   │   └── model_summary.py # Console summary for model architecture and metrics
│   │   └── training/ # Training orchestration code
│   │       └── model_trainer.py # Model compilation, callbacks, and fit loop orchestration
└── tests/ # Automated unit and regression tests
  ├── test_cli.py # CLI parsing, dispatch, and error handling tests
  ├── test_config.py # Configuration loading and access tests
  ├── test_coverage_gaps.py # Defensive branch and coverage tests
  ├── test_data.py # Corpus loading and dataset construction tests
  ├── test_entrypoints.py # Application and interface entrypoint tests
  ├── test_generation.py # Sampling and text-generation tests
  ├── test_logger.py # Logger reuse and handler configuration tests
  ├── test_models.py # Transformer shape and output tests
  ├── test_pipeline.py # Pipeline loading, generation, and plotting tests
  ├── test_reporting.py # Report, chart, and model-summary tests
  └── test_training.py # Trainer construction, compilation, and callback tests
```

## 📋 Main configuration parameters

The default model configuration is defined in `src/app/configs/default.yaml`.

Relevant sections:

- `project`: name, seed, log level
- `data`: raw path, processed directory, vocabulary size, sequence length, batch size
- `model`: embedding size, heads, feed-forward size, layers, dropout rate
- `training`: epochs, learning rate, checkpoint directory, log directory
- `generation`: default prompt, tokens, temperature, top_k

## 🧪 Validation and outputs

Run the complete Python test suite from the monorepo root:

```bash
pnpm test:unit:py
```

Run the case-specific suite from this project directory:

```bash
uv run pytest
```

The tests cover all Python modules under `src/` without requiring a new training run.

After training, the project generates:

- model checkpoints in `outputs/checkpoints/`
- training metrics in `outputs/logs/`
- processed vocabulary in `outputs/data/processed/`
- generation reports and plots in `outputs/reports/`

The generated files are runtime artifacts and should not be committed to source control.

## 🔎 Typical full workflow

```bash
pnpm build:train
pnpm build:generate
pnpm build:report
pnpm build:with:interface # Optional
```

This is the recommended order for a complete local run of the Shakespeare Transformer case, with all runtime outputs stored under the `outputs/` hierarchy.
