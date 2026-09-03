"""Utilities to plot training loss and accuracy curves."""

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from src.app.logger import Logger

logger = Logger().get_logger(name="core.history_plotter", level="INFO")

sns.set_theme(style="whitegrid", context="talk")
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"


class HistoryPlotter:
    """Create plot files from a Keras-like history object for model diagnostics."""

    PROJECT_ROOT = Path(__file__).resolve().parents[3]

    def __init__(self, history: Any | dict[str, Any], output_dir: str | Path = "outputs/reports/figures") -> None:
        """Normalize the history payload and create a project-aware output directory."""
        self.history = self._as_mapping(history)
        self.output_dir = self._resolve_output_dir(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Plot output directory ready: %s", self.output_dir)

    @staticmethod
    def _as_mapping(history: Any) -> dict[str, Any]:
        """Accept either a plain dict or a Keras-like history object."""
        if isinstance(history, dict):
            return {key: np.asarray(value).tolist() for key, value in history.items()}
        if hasattr(history, "history") and isinstance(history.history, dict):
            return {key: np.asarray(value).tolist() for key, value in history.history.items()}
        raise TypeError("HistoryPlotter requires a dict or a Keras-like history object.")

    @classmethod
    def _resolve_output_dir(cls, output_dir: str | Path) -> Path:
        """Resolve relative paths against the project root."""
        path = Path(output_dir)
        if path.is_absolute():
            return path
        return (cls.PROJECT_ROOT / path).resolve()

    def plot_loss(self, filename: str = "loss_curve.png") -> Path:
        """Save the training and validation loss curve."""
        if "loss" not in self.history:
            raise KeyError("The history mapping does not contain a 'loss' series.")

        fig, ax = plt.subplots(figsize=(10, 6))

        train_loss = np.asarray(self.history["loss"], dtype=float)
        epochs = np.arange(1, len(train_loss) + 1)
        ax.plot(epochs, train_loss, label="Train Loss", linewidth=2)
        if "val_loss" in self.history:
            val_loss = np.asarray(self.history["val_loss"], dtype=float)
            ax.plot(np.arange(1, len(val_loss) + 1), val_loss, label="Validation Loss", linewidth=2)

        ax.set_title("Training & Validation Loss", fontsize=16, pad=15)
        ax.set_xlabel("Epoch")
        ax.set_ylabel("Loss")
        ax.legend()
        ax.grid(True, alpha=0.3)

        path = self.output_dir / filename
        fig.tight_layout()
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info("Saved loss curve → %s", path)
        return path

    def plot_accuracy(self, filename: str = "accuracy_curve.png") -> Path:
        """Save the training and validation accuracy curve."""
        fig, ax = plt.subplots(figsize=(10, 6))

        if "accuracy" in self.history:
            train_accuracy = np.asarray(self.history["accuracy"], dtype=float)
            ax.plot(np.arange(1, len(train_accuracy) + 1), train_accuracy, label="Train Accuracy", linewidth=2)
        if "val_accuracy" in self.history:
            val_accuracy = np.asarray(self.history["val_accuracy"], dtype=float)
            ax.plot(np.arange(1, len(val_accuracy) + 1), val_accuracy, label="Validation Accuracy", linewidth=2)

        ax.set_title("Training & Validation Accuracy", fontsize=16, pad=15)
        ax.set_xlabel("Epoch")
        ax.set_ylabel("Accuracy")
        ax.legend()
        ax.grid(True, alpha=0.3)

        path = self.output_dir / filename
        fig.tight_layout()
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info("Saved accuracy curve → %s", path)
        return path

    def plot_all(self) -> None:
        """Generate the standard training plots."""
        try:
            loss_path = self.plot_loss()
            accuracy_path = self.plot_accuracy()
            logger.info("Saved loss curve → %s", loss_path)
            logger.info("Saved accuracy curve → %s", accuracy_path)
        except Exception as exc:  # pragma: no cover - plotting is diagnostic, but should be traceable.
            logger.exception("Failed to create training plots: %s", exc)
            raise
