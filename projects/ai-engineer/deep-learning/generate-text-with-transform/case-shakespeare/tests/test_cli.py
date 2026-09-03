from unittest.mock import Mock, patch

import pytest

from src.app.cli import CLI


def test_cli_parser_accepts_generation_options() -> None:
    with patch("sys.argv", ["case-shakespeare", "generate", "--prompt", "hello", "--tokens", "4"]):
        args = CLI().parser.parse_args()

    assert args.command == "generate"
    assert args.prompt == "hello"
    assert args.tokens == 4


def test_cli_run_dispatches_report_command() -> None:
    pipeline = Mock()
    pipeline.create_generation_report.return_value = "report.md"

    with (
        patch("sys.argv", ["case-shakespeare", "report", "--prompt", "hello"]),
        patch("src.app.cli.Pipeline", return_value=pipeline),
    ):
        CLI().run()

    pipeline.create_generation_report.assert_called_once_with(prompt="hello")


def test_cli_run_converts_missing_artifact_to_system_exit() -> None:
    cli = CLI()
    with (  # noqa: SIM117
        patch("sys.argv", ["case-shakespeare", "generate"]),
        patch("src.app.cli.Pipeline", side_effect=FileNotFoundError("missing")),
    ):
        with pytest.raises(SystemExit) as error:
            cli.run()

    assert error.value.code == 1
