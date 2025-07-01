# src/api/search.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.session import SessionLocal
from db.models import Flashcard

router = APIRouter(prefix="/search", tags=["search"])

class SearchRequest(BaseModel):
    query: str
    k: int = 5

@router.post("/", response_model=list[dict])
async def search(req: SearchRequest):
    """
    Search flashcards by substring match on question text.
    Returns up to `req.k` flashcards whose question contains the query.
    """
    try:
        with SessionLocal() as session:
            cards = (
                session.query(Flashcard)
                       .filter(Flashcard.question.contains(req.query))
                       .limit(req.k)
                       .all()
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return [
        {"id": c.id, "question": c.question, "answer": c.answer, "source": c.source}
        for c in cards
    ]
