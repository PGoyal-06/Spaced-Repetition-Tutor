import pytest

from ingest.chunker import chunk_text, count_tokens

def test_chunk_short_text():
    text = "Just a short sentence."
    chunks = chunk_text(text, max_tokens=50, overlap=10)
    assert len(chunks) == 1
    assert "Just a short sentence." in chunks[0]

def test_chunk_overlap():
    # build 3 identical sentences, each ~60 tokens long
    words = "word " * 60
    text = ". ".join([words] * 3)
    chunks = chunk_text(text, max_tokens=50, overlap=10)

    # should split into at least 2 chunks
    assert len(chunks) >= 2

    # last 10 tokens of chunk 0 == first 10 tokens of chunk 1
    tokens1 = chunks[0].split()[-10:]
    tokens2 = chunks[1].split()[:10]
    assert tokens1 == tokens2

def test_chunk_max_token_limit():
    # ensure no chunk exceeds the max_tokens
    text = "test " * 300
    chunks = chunk_text(text, max_tokens=100, overlap=20)
    assert all(count_tokens(c) <= 100 for c in chunks)
