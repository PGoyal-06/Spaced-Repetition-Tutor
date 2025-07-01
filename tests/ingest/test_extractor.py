# tests/ingest/test_extractor.py

import pytest
from pathlib import Path
from ingest.extractor import extract_text

def test_extract_two_page_sample():
    sample = Path(__file__).parent / "data" / "two_page.pdf"
    text = extract_text(str(sample))

    # Should contain the real title and a known subtitle from page 1
    assert "ChatGPT Prompts to Learn Fast(er)!" in text
    assert "Make Into a Game" in text

    # Pages are separated by at least one blank line
    assert "\n\n" in text

def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        extract_text("does_not_exist.pdf")
