# tests/ingest/test_generator.py

import json
import pytest
from unittest.mock import patch
from ingest.generator import generate_flashcard

# Fixture to mock the OpenAI v1 chat.completions.create
@pytest.fixture
def mock_openai(monkeypatch):
    args_dict = {
        "question": "What is photosynthesis?",
        "answer":   "Photosynthesis converts light energy into chemical energy.",
        "source":   "chunk-001"
    }

    class DummyFC:
        def __init__(self, arguments):
            self.arguments = arguments

    class DummyMsg:
        def __init__(self, fc):
            self.function_call = fc

    class DummyChoice:
        def __init__(self, msg):
            self.message = msg

    class DummyResp:
        def __init__(self, data):
            json_args = json.dumps(data)
            fc = DummyFC(json_args)
            msg = DummyMsg(fc)
            self.choices = [DummyChoice(msg)]

    # Monkeypatch the chat completions endpoint
    monkeypatch.setattr(
        'openai.chat.completions.create',
        lambda *args, **kwargs: DummyResp(args_dict)
    )
    return args_dict


def test_generate_flashcard_returns_valid_structure(mock_openai):
    chunk = "Plants use sunlight to make sugars via photosynthesis."
    card = generate_flashcard(chunk, source_id="chunk-001")

    assert isinstance(card, dict)
    assert set(card.keys()) == {"question", "answer", "source"}
    assert card["source"] == "chunk-001"
    assert "photosynthesis" in card["answer"].lower()

@patch('openai.chat.completions.create')
def test_generate_flashcard_called_with_function(mock_create):
    # Stub return value
    mock_create.return_value = type('R', (), {'choices': []})()
    # Call function
    generate_flashcard("Sample text.", source_id="chunk-xyz")
    # Verify the chat endpoint was invoked
    mock_create.assert_called()
