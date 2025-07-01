#!/usr/bin/env python3
# scripts/generate_all_flashcards.py

from ingest.generator import generate_flashcard
from ingest.storage import store_flashcard
from db.session import SessionLocal
from db.models import Chunk
from ingest.utils import jaccard


def main():
    """
    Batch-generate flashcards for every stored Chunk, deduplicating
    on question text (Jaccard similarity > 0.8), and persist them.
    """
    session = SessionLocal()
    seen_questions: list[str] = []

    for chunk in session.query(Chunk).all():
        # Generate a flashcard from this chunk
        card = generate_flashcard(chunk.text, source_id=str(chunk.id))
        question = card["question"]

        # Skip if this question is too similar to one we’ve already stored
        if any(jaccard(question, prev_q) > 0.8 for prev_q in seen_questions):
            continue

        # Persist the flashcard
        store_flashcard(
            question=question,
            answer=card["answer"],
            source=card["source"]
        )
        seen_questions.append(question)

    session.close()
    print("✅ All flashcards generated and stored.")


if __name__ == "__main__":
    main()
