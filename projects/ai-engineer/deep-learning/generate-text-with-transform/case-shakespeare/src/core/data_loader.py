"""Responsible for loading the raw Shakespeare corpus."""

from pathlib import Path

from src.app.logger import Logger


class TextLoader:
    """Load the raw text corpus from a project-aware file path."""

    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    def __init__(self, file_path: str | Path) -> None:
        """Resolve and validate the corpus path at initialization time."""
        # Resolve paths from the project root so loading is independent from the current working directory.
        self.file_path = self._resolve_path(file_path)
        self.logger = Logger().get_logger(name="core.data_loader", level="INFO")

    @classmethod
    def _resolve_path(cls, file_path: str | Path) -> Path:
        """Resolve relative paths against the project root to keep execution stable."""
        path = Path(file_path)
        if path.is_absolute():
            return path
        return (cls.PROJECT_ROOT / path).resolve()

    def load(self) -> str:
        """Return the corpus content as a single UTF-8 string."""
        if not self.file_path.exists():
            message = (
                f"Shakespeare corpus not found at: {self.file_path.resolve()}\n"
                "Please place 'shakespeare.txt' inside the 'data/raw/' directory."
            )
            self.logger.error(message)
            raise FileNotFoundError(message)

        try:
            content = self.file_path.read_text(encoding="utf-8")
        except OSError as exc:
            self.logger.exception("Failed to read corpus file: %s", self.file_path)
            raise RuntimeError(f"Unable to read corpus file: {self.file_path}") from exc

        self.logger.info("Loaded corpus from %s (%s characters)", self.file_path, f"{len(content):,}")
        return content
