from db.session import SessionLocal
from db.models import Chunk, Document, Flashcard, Review
from ingest.embeddings import embed
from datetime import datetime, timedelta

def store_chunk(text: str, doc_title: str) -> None:
    with SessionLocal() as session:
        doc = session.query(Document).filter_by(title=doc_title).first()
        if not doc:
            doc = Document(title=doc_title)
            session.add(doc)
            session.commit()
        vec = embed(text)
        chunk = Chunk(document_id=doc.id, text=text, embedding=vec)
        session.add(chunk)
        session.commit()

def find_similar(query: str, k: int = 5) -> list[Chunk]:
    qvec = embed(query)
    with SessionLocal() as session:
        return (
            session.query(Chunk)
                   .order_by(Chunk.embedding.cosine_distance(qvec))
                   .limit(k)
                   .all()
        )

def store_flashcard(question: str, answer: str, source: str, doc_title: str | None = None) -> int:
    with SessionLocal() as session:
        doc_id = None
        if doc_title:
            doc = session.query(Document).filter_by(title=doc_title).first()
            if not doc:
                doc = Document(title=doc_title)
                session.add(doc)
                session.commit()
            doc_id = doc.id
        card = Flashcard(
            question=question,
            answer=answer,
            source=source,
            document_id=doc_id
        )
        session.add(card)
        session.commit()
        return card.id

def store_review(user_id: int, flashcard_id: int, quality: int) -> dict:
    """
    Record a review and compute SM-2 scheduling.
    Returns dict with: flashcard_id, quality, ease_factor,
    interval_days and next_due (ISO string).
    """
    now = datetime.utcnow()
    with SessionLocal() as session:
        last = (
            session.query(Review)
                   .filter_by(user_id=user_id, flashcard_id=flashcard_id)
                   .order_by(Review.timestamp.desc())
                   .first()
        )
        # initial
        if not last:
            ease_factor   = 2.5
            interval_days = 1
        else:
            delta = 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
            ease_factor = max(1.3, last.ease_factor + delta)
            interval_days = 1 if last.interval_days == 0 else int(round(last.interval_days * ease_factor))

        next_due = now + timedelta(days=interval_days)
        review = Review(
            user_id=user_id,
            flashcard_id=flashcard_id,
            quality=quality,
            ease_factor=ease_factor,
            interval_days=interval_days,
            next_due=next_due,
            timestamp=now
        )
        session.add(review)
        session.commit()
        return {
            "flashcard_id": flashcard_id,
            "quality": quality,
            "ease_factor": ease_factor,
            "interval_days": interval_days,
            "next_due": next_due.isoformat(),
        }
