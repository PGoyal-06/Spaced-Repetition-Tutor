# tests/test_pipeline.py

import json
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient

from main import app
from ingest.extractor import extract_text
from ingest.cleaner import clean_text
from ingest.chunker import chunk_text

client = TestClient(app)

def test_full_flow(tmp_path):
    # 1. Copy a small PDF fixture into tmp_path
    fixture = Path("tests/ingest/data/two_page.pdf")
    test_pdf = tmp_path / "sample.pdf"
    test_pdf.write_bytes(fixture.read_bytes())

    # 2. Ingest → clean → chunk
    raw = extract_text(str(test_pdf))
    clean = clean_text(raw)
    chunks = chunk_text(clean, max_tokens=50, overlap=10)
    assert chunks, "No chunks generated"

    # 3. Generate & store flashcards for first 2 chunks
    for i, c in enumerate(chunks[:2], start=1):
        resp = client.post("/flashcards/generate/", json={
            "chunk_id": str(i),
            "text": c
        })
        assert resp.status_code == 200
        body = resp.json()
        # flashcard_id should be an int
        assert isinstance(body.get("flashcard_id"), int)
        assert body["question"]
        assert body["answer"]
        assert body["source"] == str(i)

    # 4. Search for something that definitely appears
    resp = client.post("/search/", json={"query": chunks[0], "k": 2})
    assert resp.status_code == 200
    results = resp.json()
    assert isinstance(results, list)
    # returned texts should match at least one flashcard text
    assert any(chunks[0] in card.get("text", card.get("question", "")) for card in results)
