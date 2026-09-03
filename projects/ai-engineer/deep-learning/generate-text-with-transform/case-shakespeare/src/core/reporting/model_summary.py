"""Utilities for inspecting model size and parameter counts."""

from pathlib import Path

import tensorflow as tf
from rich.console import Console
from rich.table import Table

console = Console()


class ModelSummary:
    """Display a compact summary of parameter counts and model size."""

    def __init__(self, model: tf.keras.Model) -> None:
        """Store the model object used for metrics and display."""
        self.model = model

    @property
    def total_params(self) -> int:
        """Return the total number of parameters in the model."""
        return self.model.count_params()

    @property
    def trainable_params(self) -> int:
        """Return the number of trainable parameters only."""
        return sum(tf.keras.backend.count_params(weight) for weight in self.model.trainable_weights)

    def size_in_mb(self, model_path: Path | None = None) -> float:
        """Return the estimated model size in MB."""
        if model_path and model_path.exists():
            return model_path.stat().st_size / (1024 * 1024)
        return (self.total_params * 4) / (1024 * 1024)

    def display(self, model_path: Path | None = None) -> None:
        """Print the summary table in a readable format."""
        table = Table(title="Model Information", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="bold")
        table.add_column("Value", style="green")

        table.add_row("Total parameters", f"{self.total_params:,}")
        table.add_row("Trainable parameters", f"{self.trainable_params:,}")
        table.add_row("Estimated size (MB)", f"{self.size_in_mb(model_path):.2f}")

        console.print(table)
