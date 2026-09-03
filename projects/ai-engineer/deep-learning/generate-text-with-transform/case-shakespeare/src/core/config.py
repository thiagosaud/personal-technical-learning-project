"""Project configuration loader and project-root path resolution."""

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml
from rich.console import Console
from rich.table import Table

console = Console()


class ProjectConfig:
    """Load, validate, and expose the YAML configuration for the Shakespeare project."""

    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    def __init__(self, config_path: str | Path = "src/app/configs/default.yaml") -> None:
        """Resolve the configuration file and load it into memory."""
        self.path = self._resolve_path(config_path)

        if not self.path.exists():
            # The project may be launched from a different cwd; keep project-root resolution safe.
            fallback = self.PROJECT_ROOT / "src" / "app" / "configs" / "default.yaml"
            if fallback.exists():
                self.path = fallback
            else:
                raise FileNotFoundError(f"Config file not found: {self.path.resolve()}")

        with self.path.open("r", encoding="utf-8") as config_file:
            loaded_config = yaml.safe_load(config_file) or {}
            if not isinstance(loaded_config, dict):
                raise ValueError(f"Configuration in {self.path} must define a dictionary at the root level.")
            self._data: dict[str, Any] = loaded_config

    @classmethod
    def _resolve_path(cls, candidate: str | Path) -> Path:
        """Resolve project-relative paths against the workspace root."""
        path = Path(candidate)
        if path.is_absolute():
            return path
        return (cls.PROJECT_ROOT / path).resolve()

    def resolve_path(self, candidate: str | Path) -> Path:
        """Resolve an arbitrary runtime path using the project root."""
        return self._resolve_path(candidate)

    def get_path(self, *keys: str) -> Path:
        """Resolve a nested path value such as ('data', 'raw_path')."""
        value = self.get(*keys)
        if value is None:
            raise KeyError(f"No path configured for {'/'.join(keys)}")
        return self.resolve_path(value)

    @property
    def project(self) -> dict[str, Any]:
        """Return the top-level project section."""
        return self._data["project"]

    @property
    def data(self) -> dict[str, Any]:
        """Return data ingestion and preprocessing settings."""
        return self._data["data"]

    @property
    def model(self) -> dict[str, Any]:
        """Return model architecture settings."""
        return self._data["model"]

    @property
    def training(self) -> dict[str, Any]:
        """Return training hyperparameters and callbacks settings."""
        return self._data["training"]

    @property
    def generation(self) -> dict[str, Any]:
        """Return text-generation parameters."""
        return self._data["generation"]

    def get(self, *keys: str, default: Any = None) -> Any:
        """Get a nested key from the configuration dictionary safely."""
        node: Any = self._data
        for key in keys:
            if not isinstance(node, dict) or key not in node:
                return default
            node = node[key]
        return node

    def display(self, title: str = "Current Configuration") -> None:
        """Render the config in a Rich table for terminal inspection."""
        table = Table(title=title, show_header=True, header_style="bold cyan")
        table.add_column("Section", style="bold")
        table.add_column("Parameter")
        table.add_column("Value", style="green")

        for section, values in self._data.items():
            if not isinstance(values, dict):
                continue

            first = True
            for key, value in values.items():
                table.add_row(section if first else "", key, str(value))
                first = False

        console.print(table)

    def interactive_override(self) -> None:
        """Allow a small set of commonly edited config entries to be overridden interactively."""
        console.print("\n[bold yellow]Interactive parameter override[/bold yellow]")
        console.print("Press Enter to keep the current value.\n")

        editable = [
            ("data", "vocab_size", int),
            ("data", "seq_length", int),
            ("data", "batch_size", int),
            ("model", "num_layers", int),
            ("model", "embed_dim", int),
            ("training", "epochs", int),
            ("training", "learning_rate", float),
            ("generation", "default_prompt", str),
            ("generation", "num_tokens", int),
            ("generation", "temperature", float),
            ("generation", "top_k", int),
        ]

        for section, key, value_type in editable:
            current = self._data[section][key]
            user_input = console.input(f"  {section}.{key} [{current}]: ").strip()
            if user_input:
                try:
                    self._data[section][key] = value_type(user_input)
                except ValueError:
                    console.print(f"  [red]Invalid value, keeping {current}[/red]")

        console.print("\n[green]Configuration updated.[/green]")
        self.display(title="Updated Configuration")

    def to_dict(self) -> dict[str, Any]:
        """Return a deep copy to avoid accidental mutation of the config object."""
        return deepcopy(self._data)
