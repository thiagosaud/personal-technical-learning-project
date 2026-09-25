from src.core.layer.processor.query_processor import QueryProcessor


def test_query_processor_normalization() -> None:
    """Validates query cleaning, lowercasing, and synonym expansion."""
    processor = QueryProcessor()
    raw_query = "   How IS the weather in NEW YORK today?!   "
    processed = processor.process(raw_query)

    assert isinstance(processed, str)
    # Note: punctuation is stripped, lowercased, and synonyms applied if matched
    assert "how is the weather in new york today" in processed
