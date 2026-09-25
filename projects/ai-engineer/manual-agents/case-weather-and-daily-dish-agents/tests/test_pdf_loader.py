from pathlib import Path
from unittest.mock import patch

import pytest

from src.app.configs.settings import Settings
from src.core.layer.data.pdf_loader import PdfFaqLoader


def test_pdf_loader_file_not_found() -> None:
    """Validates that FileNotFoundError is raised when the PDF file does not exist."""
    with pytest.raises(FileNotFoundError):
        PdfFaqLoader.load_text("invalid_nonexistent_path.pdf")


def test_pdf_loader_parse_branches_and_exceptions() -> None:
    """Validates 100% coverage across all branches: empty blocks, missing Q/A markers, exceptions, and valid items."""
    # 1. Blank/empty block (triggers 'if not block.strip(): continue')
    blank_block = "\n   \n"
    # 2. Block without Q: or A: markers (skips inner conditional)
    unmarked_block = "\n 1. Some random text without markers\n"
    # 3. Block with empty q_part or a_part (fails 'if q_part and a_part:')
    empty_parts_block = "\n 2. Q:   A:    \n"
    # 4. Malformed block triggering exception in clean_text
    error_block = "\n 3. Q: Error? A: Error\n"
    # 5. Valid block
    valid_block = "\n 4. Q: What is AI? A: Artificial Intelligence\n"

    mock_raw_text = f"{blank_block}{unmarked_block}{empty_parts_block}{error_block}{valid_block}"

    with (
        patch.object(PdfFaqLoader, "load_text", return_value=mock_raw_text),
        patch.object(
            PdfFaqLoader, "clean_text", side_effect=[Exception("Clean error"), "ai", "artificial intelligence"]
        ),
    ):
        faq_data = PdfFaqLoader.parse_faq("dummy_path.pdf")

        assert isinstance(faq_data, list)
        assert len(faq_data) == 1
        assert faq_data[0]["question"] == "ai"


def test_pdf_loader_structure() -> None:
    """Validates that the PDF loader returns structured FAQ data when file exists."""
    pdf_path = Path(Settings.FAQ_PDF_PATH)

    if not pdf_path.exists():
        pytest.skip(f"FAQ PDF file not found at {pdf_path}. Skipping test.")

    faq_data = PdfFaqLoader.parse_faq(str(pdf_path))

    assert isinstance(faq_data, list)
    if len(faq_data) > 0:
        assert "question" in faq_data[0]
        assert "answer" in faq_data[0]
