import re

import pytest

from ingest.cleaner import clean_text

def test_fix_mojibake():
    raw = "This â€“ is â€œweirdâ€� text."
    cleaned = clean_text(raw)
    assert "–" in cleaned
    assert "“weird”" in cleaned

def test_remove_repeated_lines():
    raw = "HEADER\nA\nB\nHEADER\nC\nHEADER\n"
    cleaned = clean_text(raw)
    # repeated "HEADER" lines should be removed
    assert "HEADER" not in cleaned
    # original unique lines should remain
    assert "A" in cleaned and "B" in cleaned and "C" in cleaned

def test_whitespace_normalization():
    raw = "Line1   with   spaces\n\n\nLine2"
    cleaned = clean_text(raw)
    # internal spaces collapsed
    assert "Line1 with spaces" in cleaned
    # no more than two consecutive newlines
    assert "\n\n" in cleaned and "\n\n\n" not in cleaned
