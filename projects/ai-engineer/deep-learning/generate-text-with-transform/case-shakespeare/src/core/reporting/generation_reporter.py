"""Markdown generation report for prompt comparisons across temperatures."""

from datetime import datetime
from pathlib import Path

from src.core.generation.text_generator import TextGenerator


class GenerationReporter:
    """Generate a markdown report comparing text generation under different temperatures."""

    PROJECT_ROOT = Path(__file__).resolve().parents[3]

    def __init__(
        self,
        generator: TextGenerator,
        output_dir: str | Path = "outputs/reports/generation",
    ) -> None:
        """Store the generator and ensure the report directory exists."""
        self.generator = generator
        self.output_dir = self._resolve_output_dir(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _resolve_output_dir(cls, output_dir: str | Path) -> Path:
        """Resolve relative paths against the project root."""
        path = Path(output_dir)
        if path.is_absolute():
            return path
        return (cls.PROJECT_ROOT / path).resolve()

    def generate_report(
        self,
        prompt: str,
        temperatures: list[float] | None = None,
        num_tokens: int = 200,
        top_k: int = 40,
    ) -> Path:
        """Save a text-generation comparison report to disk."""
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty when generating a report.")
        if num_tokens < 0:
            raise ValueError("Number of generated tokens cannot be negative.")
        if temperatures is None:
            temperatures = [0.5, 0.7, 0.9, 1.1]

        # Create a timestamped filename so each report remains traceable and reproducible.
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.output_dir / f"generation_report_{timestamp}.md"

        lines = [
            "# Shakespeare Transformer - Generation Report",
            "",
            f"**Prompt:** `{prompt}`",
            f"**Tokens generated:** {num_tokens}",
            f"**Top-k:** {top_k}",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
        ]

        # Generate text across the configured temperature values and compare the resulting samples.
        for temperature in temperatures:
            text = self.generator.generate(
                start_string=prompt,
                num_generate=num_tokens,
                temperature=temperature,
                top_k=top_k,
            )

            lines.append(f"## Temperature = {temperature}")
            lines.append("")
            lines.append("```")
            lines.append(text)
            lines.append("```")
            lines.append("")

        report_path.write_text("\n".join(lines), encoding="utf-8")
        return report_path
