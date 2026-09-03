from unittest.mock import Mock, patch


def test_main_delegates_to_cli_main() -> None:
    with patch("src.main.main") as main:
        import src.main

        src.main.main()

    main.assert_called_once()


def test_gradio_generate_function_uses_pipeline() -> None:
    pipeline = Mock()
    pipeline.generate.return_value = "generated"

    with patch("src.app.infrastructure.gradio_app.Pipeline", return_value=pipeline):
        from src.app.infrastructure.gradio_app import create_interface

        interface = create_interface()

    assert interface is not None
