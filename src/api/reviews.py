# src/api/reviews.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import func, and_
from db.session import SessionLocal
from db.models import Flashcard, Review
from ingest.storage import store_review

router = APIRouter(prefix="/reviews", tags=["reviews"])


class ReviewRequest(BaseModel):
    user_id: int
    quality: int


@router.post("/{flashcard_id}", response_model=dict)
async def submit_review(
    flashcard_id: int,
    req: ReviewRequest
):
    """
    Record a review for `flashcard_id` at quality=req.quality,
    and return the new schedule info.
    """
    try:
        result = store_review(
            user_id=req.user_id,
            flashcard_id=flashcard_id,
            quality=req.quality
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


@router.get("/next", response_model=dict)
async def next_review(user_id: int):
    """
    Return the next flashcard due for review for this user.
    New (unreviewed) cards are returned first; otherwise
    returns the reviewed card whose next_due is soonest (and ≤ now).
    """
    now = datetime.utcnow()

    try:
        with SessionLocal() as session:
            # --- 1) Unreviewed cards ---
            # subquery of flashcard_ids the user has reviewed
            reviewed_ids = (
                session.query(Review.flashcard_id)
                       .filter(Review.user_id == user_id)
                       .distinct()
                       .subquery()
            )
            # first flashcard NOT in that list:
            unrev = (
                session.query(Flashcard)
                       .filter(~Flashcard.id.in_(reviewed_ids))
                       .order_by(Flashcard.id)
                       .first()
            )
            if unrev:
                return {
                    "id":       unrev.id,
                    "question": unrev.question,
                    "answer":   unrev.answer,
                    "source":   unrev.source,
                    # brand-new cards are "due now"
                    "next_due": now.isoformat(),
                }

            # --- 2) Among reviewed cards, find earliest due ---
            # Subquery: for each flashcard, the max timestamp of this user's reviews
            subq = (
                session.query(
                    Review.flashcard_id,
                    func.max(Review.timestamp).label("last_ts")
                )
                .filter(Review.user_id == user_id)
                .group_by(Review.flashcard_id)
                .subquery()
            )
            # Join back to get only those latest-rows
            latest_reviews = (
                session.query(Review)
                       .join(
                           subq,
                           and_(
                               Review.flashcard_id == subq.c.flashcard_id,
                               Review.timestamp == subq.c.last_ts
                           )
                )
            )
            # Filter for due now or earlier, order by next_due
            due = (
                latest_reviews
                .filter(Review.next_due <= now)
                .order_by(Review.next_due.asc())
                .first()
            )
            if not due:
                # no cards due
                return {}

            card = due.flashcard
            return {
                "id":       card.id,
                "question": card.question,
                "answer":   card.answer,
                "source":   card.source,
                "next_due": due.next_due.isoformat(),
            }

    except Exception as e:
        # Log/inspect server logs for the full traceback
        raise HTTPException(status_code=500, detail=str(e))
