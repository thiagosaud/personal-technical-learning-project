"""Command-line interface for the Shakespeare text-generation project."""

import argparse
import sys
from pathlib import Path

from src.app.logger import Logger
from src.app.pipeline import Pipeline

# Resolve the project root from this file and expose it on PYTHONPATH for local imports.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class CLI:
    """Expose the training, generation, and report commands for the project."""

    _DEFAULT_CONFIG_PATH = ROOT / "configs" / "default.yaml"

    def __init__(self) -> None:
        # The CLI owns the parser and logger so every command has a consistent trace.
        self.parser = self._build_parser()
        self.logger_factory = Logger()
        self.logger = self.logger_factory.get_logger(name="app.cli", level="INFO")

    def _build_parser(self) -> argparse.ArgumentParser:
        """Build the command tree for train, generation, and report modes."""

        # The parser is configured to provide help text and default values for each command.
        parser = argparse.ArgumentParser(
            description="Shakespeare Transformer CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        # Subparsers allow for different commands with their own arguments.
        subparsers = parser.add_subparsers(dest="command", required=True)

        # Train command allows for optional interactive mode and config path.
        train_parser = subparsers.add_parser("train", help="Train the model")
        train_parser.add_argument("--config", default=self._DEFAULT_CONFIG_PATH)
        train_parser.add_argument("--interactive", action="store_true")

        # Generation command allows for optional prompt and generation parameters.
        generate_parser = subparsers.add_parser("generate", help="Generate text")
        generate_parser.add_argument("--config", default=self._DEFAULT_CONFIG_PATH)
        generate_parser.add_argument("--interactive", action="store_true")
        generate_parser.add_argument("--prompt", type=str, default=None)
        generate_parser.add_argument("--tokens", type=int, default=None)
        generate_parser.add_argument("--temperature", type=float, default=None)
        generate_parser.add_argument("--top_k", type=int, default=None)

        # Report command generates a Markdown report of generations at different temperatures.
        report_parser = subparsers.add_parser("report", help="Generate a Markdown report")
        report_parser.add_argument("--config", default=self._DEFAULT_CONFIG_PATH)
        report_parser.add_argument("--prompt", type=str, default=None)

        return parser

    def run(self) -> None:
        """Execute the selected command from the CLI arguments."""
        try:
            # Parse the command-line arguments and dispatch to the appropriate pipeline method.
            args = self.parser.parse_args()
            self.logger.info("Starting command: %s", args.command)
            pipeline = Pipeline(config_path=args.config)

            # Dispatch to the appropriate command based on the parsed arguments.
            if args.command == "train":
                pipeline.train(interactive=args.interactive)
            elif args.command == "generate":
                pipeline.generate(
                    prompt=args.prompt,
                    num_tokens=args.tokens,
                    temperature=args.temperature,
                    top_k=args.top_k,
                    interactive=args.interactive,
                )
            elif args.command == "report":
                report_path = pipeline.create_generation_report(prompt=args.prompt)
                self.logger.info("Report saved to: %s", report_path)
            else:
                self.logger.warning("No valid command selected; showing help text.")
                self.parser.print_help()

        # Handle exceptions gracefully and log them for debugging.
        except FileNotFoundError as exc:
            self.logger.exception("A required file or model artifact was not found: %s", exc)
            raise SystemExit(1) from exc
        except ValueError as exc:
            self.logger.exception("Invalid CLI input or generation configuration: %s", exc)
            raise SystemExit(1) from exc
        except Exception as exc:
            self.logger.exception("Unexpected CLI failure: %s", exc)
            raise SystemExit(1) from exc


def main() -> None:
    """Entry point used by the package script and python -m invocation."""
    CLI().run()


if __name__ == "__main__":
    main()
