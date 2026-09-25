import re
from pathlib import Path

from pypdf import PdfReader

from src.core.layer.logging.app_logger import AppLogger


class PdfFaqLoader:
    """Responsible for safely extracting and parsing FAQ structured blocks from local PDF documents under data/raw/."""

    _logger = AppLogger.get_logger("PdfFaqLoader")

    @staticmethod
    def load_text(pdf_path: str) -> str:
        """
        Extracts raw text strings from all pages of a local PDF file located in data/raw/.

        Args:
            pdf_path (str): The filesystem path to the local PDF file.

        Returns:
            str: Concatenated raw text content.
        """
        path_obj = Path(pdf_path)

        if not path_obj.exists():
            PdfFaqLoader._logger.error("Local FAQ PDF file not found at path: %s", pdf_path)
            raise FileNotFoundError(f"The FAQ PDF file was not found at: {pdf_path}")

        PdfFaqLoader._logger.info("Loading text from local raw PDF file: %s", pdf_path)
        reader = PdfReader(str(path_obj))
        return "".join([page.extract_text() for page in reader.pages])

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Normalizes whitespaces and cleans text content.

        Args:
            text (str): Raw text string to clean.

        Returns:
            str: Cleaned and normalized string.
        """
        return " ".join(text.split())

    @classmethod
    def parse_faq(cls, pdf_path: str) -> list[dict[str, str]]:
        """
        Parses FAQ text blocks from a local PDF using deterministic line splitting to prevent backtracking.

        Args:
            pdf_path (str): Target local PDF file path.

        Returns:
            List[Dict[str, str]]: Structured list containing question and answer dictionaries.
        """
        raw_text = cls.load_text(pdf_path)
        raw_blocks = re.split(r"\n\s*\d+\.\s*", raw_text)

        faq_pairs: list[dict[str, str]] = []
        for index, block in enumerate(raw_blocks):
            if not block.strip():
                continue

            if "Q:" in block and "A:" in block:
                try:
                    parts = block.split("A:", 1)
                    q_part = parts[0].replace("Q:", "").strip()
                    a_part = parts[1].strip()

                    if q_part and a_part:
                        faq_pairs.append({"question": cls.clean_text(q_part.lower()), "answer": cls.clean_text(a_part)})
                except Exception as e:
                    cls._logger.warning("Failed to parse FAQ block at index %d: %s", index, e)
                    continue

        cls._logger.info("Successfully parsed %d FAQ items from data/raw/ PDF.", len(faq_pairs))
        return faq_pairs
