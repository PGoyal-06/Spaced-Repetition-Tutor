from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ingest.storage import store_flashcard
from ingest.generator import generate_flashcard


router = APIRouter(prefix="/flashcards", tags=["flashcards"])

class GenCardRequest(BaseModel):
    chunk_id: str
    text: str
    doc_title: str | None = None

@router.post("/generate/", response_model=dict)
async def gen_card(req: GenCardRequest):
    """
    Generate a flashcard from a single chunk and persist it.
    Returns the new flashcard’s ID plus its content.
    """
    try:
        card = generate_flashcard(req.text, source_id=req.chunk_id)
        card_id = store_flashcard(
            question=card["question"],
            answer=card["answer"],
            source=card["source"],
            doc_title=req.doc_title,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"flashcard_id": card_id, **card}
