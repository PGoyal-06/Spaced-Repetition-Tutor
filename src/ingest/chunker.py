# src/ingest/chunker.py

import tiktoken

# Initialize the tiktoken encoder for OpenAI's embedding model
_encoder = tiktoken.get_encoding("cl100k_base")  # matches text-embedding-3-small

def chunk_text(text: str, max_tokens: int = 200, overlap: int = 50) -> list[str]:
    """
    Chunk text into overlapping token windows.

    Args:
        text: The cleaned text string to chunk.
        max_tokens: Maximum number of tokens per chunk.
        overlap: Number of tokens to overlap between consecutive chunks.

    Returns:
        List of chunk strings, each decoded from tokens.
    """
    tokens = _encoder.encode(text)
    if max_tokens <= overlap:
        raise ValueError("max_tokens must be greater than overlap")

    step = max_tokens - overlap
    chunks: list[str] = []

    for start in range(0, len(tokens), step):
        window = tokens[start : start + max_tokens]
        chunks.append(_encoder.decode(window))

    return chunks

def count_tokens(text: str) -> int:
    """
    Return the number of tokens in `text` according to tiktoken.

    Args:
        text: A string to count tokens for.
    """
    return len(_encoder.encode(text))


if __name__ == "__main__":
    # Quick manual demo
    sample = "This is a test. " * 100
    for i, c in enumerate(chunk_text(sample, max_tokens=50, overlap=10)):
        print(f"Chunk {i}: {count_tokens(c)} tokens")
