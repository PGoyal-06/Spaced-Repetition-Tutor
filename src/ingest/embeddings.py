# src/ingest/embeddings.py

import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Ensure the OpenAI API key is set
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY not set in environment")


def embed(text: str) -> list[float]:
    """
    Generate a text embedding using OpenAI's text-embedding-3-small model.

    Args:
        text: The input string to embed.
    Returns:
        A list of floats representing the embedding vector.
    """
    # Call the new v1 embeddings endpoint
    resp = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    # The CreateEmbeddingResponse has a .data list with .embedding attribute
    return resp.data[0].embedding


if __name__ == '__main__':
    demo = "Hello, world!"
    vec = embed(demo)
    print(f"Length: {len(vec)}")
    print(f"Sample: {vec[:5]}")
