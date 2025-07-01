# src/ingest/cleaner.py

import re
from ftfy import fix_text

def clean_text(raw_text: str) -> str:
    """
    Clean and normalize raw text extracted from PDFs.

    Steps:
    1. Replace common mojibake quote sequences with ASCII quotes for consistency.
    2. Fix encoding and decoding issues (mojibake) with ftfy.
    3. Convert any straight or replacement‐char quotes into curly quotes.
    4. Replace form feeds (page breaks) with newlines.
    5. Remove repeated headers/footers (lines occurring >2 times).
    6. Collapse multiple spaces/tabs and reduce excessive newlines.

    Args:
        raw_text: The raw string output from extract_text().
    Returns:
        A cleaned and normalized text string ready for chunking.
    """
    # 1. Normalize common mojibake curly-quote sequences to ASCII
    text = raw_text.replace('â€œ', '"').replace('â€�', '"')

    # 2. Fix general encoding issues and normalize Unicode
    text = fix_text(text)

    # 3. Uniformly convert any straight or replacement‐char quotes into curly quotes
    #    This handles "weird" or �weird� or “weird” variants.
    text = re.sub(r'["\ufffd]([^"\ufffd]+)["\ufffd]', r'“\1”', text)

    # 4. Replace form feeds (page breaks) with newlines
    text = text.replace('\x0c', '\n')

    # 5. Remove repeated headers/footers
    lines = text.splitlines()
    freq = {}
    for line in lines:
        freq[line] = freq.get(line, 0) + 1
    filtered = [
        line for line in lines
        if freq.get(line, 0) <= 2 or not line.strip()
    ]
    text = '\n'.join(filtered)

    # 6. Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)              # collapse spaces/tabs
    text = re.sub(r'^ +| +$', '', text, flags=re.MULTILINE)  # strip line-end spaces
    text = re.sub(r'\n{3,}', '\n\n', text)            # max two newlines

    return text

if __name__ == '__main__':
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else ''
    if not path:
        print('Usage: python cleaner.py <path_to_raw_text_file>')
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    print(clean_text(raw))
