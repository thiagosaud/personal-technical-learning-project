"""
Data Visualization Module [VISUALIZER LAYER].
Generates analytics plots using advanced overlapping repulsion algorithms.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from adjustText import adjust_text
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from config.schema.data.vehicle import VehicleSchema


class ModelVisualizerLayer:
    """Handles graphics frontend generation and saves publication-quality PNGs."""

    # Design System Constants (Enterprise UI consistency)
    _COLOR_PRIMARY = "#003366"
    _COLOR_TREND = "#D32F2F"
    _COLOR_FIT = "#2E7D32"
    _COLOR_TEXT = "#2c3e50"
    _SCATTER_SIZE = 120

    def __init__(self, data: pd.DataFrame, output_dir: Path | str = "outputs/figures") -> None:
        self.df = data
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

        self._label_style = {
            "boxstyle": "round,pad=0.15",
            "facecolor": "#ffffff",
            "alpha": 0.9,
            "edgecolor": "#dcdcdc",
            "lw": 0.5,
        }

        self._arrow_props = {"arrowstyle": "->", "color": "#7f8c8d", "lw": 0.6, "shrinkA": 3, "shrinkB": 3}

    def _create_base_plot(self, title: str, xlabel: str, ylabel: str) -> tuple[Figure, Axes]:
        """Standardizes figure setup, canvas background, and labels."""
        fig = plt.figure(figsize=(11, 6.5), facecolor="#f7f9fa")
        ax = plt.axes()
        ax.set_facecolor("#ffffff")

        plt.title(title, fontsize=12, fontweight="bold", pad=15)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        return fig, ax

    def _get_texts_config(
        self, x_series: pd.Series, y_series: pd.Series | np.ndarray
    ) -> list[tuple[float, float, str]]:
        """Extracts coordinate pairs and model names mapping for text rendering."""
        return [
            (float(x_series.iloc[i]), float(y_series[i]), str(name))
            for i, name in enumerate(self.df[VehicleSchema.MODEL.value])
        ]

    def _plot_scatter_with_labels(
        self,
        x_col: pd.Series,
        y_col: pd.Series | np.ndarray,
        label: str,
        xlim: tuple[float, float],
        ylim: tuple[float, float],
        filename: str,
        legend_loc: str = "upper left",
        force_points: tuple[float, float] | None = None,
    ) -> None:
        """DRY helper for rendering scatter dots, repulsed text labels, and persisting image."""
        plt.scatter(x_col, y_col, color=self._COLOR_PRIMARY, s=self._SCATTER_SIZE, zorder=3, label=label)

        texts_cfg = self._get_texts_config(x_col, y_col)
        texts = [
            plt.text(x, y, name, fontsize=8, fontweight="bold", color=self._COLOR_TEXT, bbox=self._label_style)
            for x, y, name in texts_cfg
        ]

        plt.xlim(xlim)
        plt.ylim(ylim)

        adjust_kwargs = {"force_text": (0.3, 0.6), "arrowprops": self._arrow_props}
        if force_points:
            adjust_kwargs["force_points"] = force_points

        adjust_text(texts, **adjust_kwargs)

        plt.legend(loc=legend_loc, frameon=True, facecolor="white")
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=300)
        plt.close()

    def generate_case1_plot(self, model, r2_score: float) -> None:
        """Generates Case 1 plot: Simple Linear Regression."""
        self._create_base_plot(
            "Case 1: Simple Linear Regression (Weight vs. Consumption)",
            "Curb Weight (KG)",
            "Energy Consumption (MJ/km)",
        )

        x_col = self.df[VehicleSchema.WEIGHT_KG.value]
        y_col = self.df[VehicleSchema.CONSUMPTION_MJ_KM.value]
        line_coords = pd.DataFrame(np.linspace(1200, 3100, 100), columns=[VehicleSchema.WEIGHT_KG.value])

        plt.plot(
            line_coords,
            model.predict(line_coords),
            color=self._COLOR_TREND,
            linestyle="--",
            linewidth=2,
            label=f"Trend Line ($R^2$: {r2_score:.2f})",
        )

        self._plot_scatter_with_labels(
            x_col=x_col,
            y_col=y_col,
            label="Real Vehicles (BYD)",
            xlim=(1200, 3100),
            ylim=(0.43, 0.98),
            filename="byd_case1_linear_simples.png",
        )

    def generate_case2_plot(self, model, r2_score: float) -> None:
        """Generates Case 2 plot: Multiple Linear Regression (Real vs. Predicted)."""
        self._create_base_plot(
            "Case 2: Multiple Linear Regression (Real vs. Predicted Acceleration)",
            "Real 0-100 km/h Acceleration time (Seconds)",
            "Model Mathematical Prediction (Seconds)",
        )

        x_col = self.df[VehicleSchema.ACCELERATION_FROM_0_TO_100.value]
        y2_pred = model.predict(self.df[[VehicleSchema.WEIGHT_KG.value, VehicleSchema.POWER_CV.value]])
        limits = [x_col.min() - 1, x_col.max() + 1]

        plt.plot(
            limits,
            limits,
            color=self._COLOR_FIT,
            linestyle=":",
            linewidth=2,
            label=f"Ideal Fit ($R^2$: {r2_score:.2f})",
        )

        self._plot_scatter_with_labels(
            x_col=x_col,
            y_col=y2_pred,
            label="Evaluated Fleet",
            xlim=(2.5, 10.5),
            ylim=(2.5, 10.5),
            filename="byd_case2_linear_multiple.png",
        )

    def generate_case3_plot(self, model, acc_score: float) -> None:
        """Generates Case 3 plot: Logistic Regression."""
        self._create_base_plot(
            "Case 3: Logistic Regression (Automatic Vehicle Classification)",
            "Battery Capacity (kWh)",
            "Pure Electric Probability (0.0 to 1.0)",
        )

        x_col = self.df[VehicleSchema.BATTERY_KWH.value]
        y_col = self.df[VehicleSchema.IS_PURE_ELECTRIC.value]
        line_coords = pd.DataFrame(np.linspace(-10, 130, 300), columns=[VehicleSchema.BATTERY_KWH.value])

        plt.plot(
            line_coords,
            model.predict_proba(line_coords)[:, 1],
            color=self._COLOR_FIT,
            linewidth=2.5,
            label=f"Sigmoid Curve (Accuracy: {acc_score:.2f})",
        )

        plt.axhline(0.5, color="gray", linestyle=":", label="Decision Boundary (50%)")

        self._plot_scatter_with_labels(
            x_col=x_col,
            y_col=y_col,
            label="Real Vehicles",
            xlim=(-10, 130),
            ylim=(-0.2, 1.2),
            filename="byd_case3_logistic.png",
            legend_loc="center right",
            force_points=(0.5, 0.8),
        )
