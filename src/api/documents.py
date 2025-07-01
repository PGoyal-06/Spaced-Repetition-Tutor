# src/api/documents.py
import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from ingest.extractor import extract_text
from ingest.cleaner import clean_text
from ingest.chunker import chunk_text
from ingest.storage import store_chunk, store_flashcard
from ingest.generator import generate_flashcard

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/", summary="Upload a lecture PDF and generate flashcards")
async def upload_and_generate(file: UploadFile = File(...)):
    # 1) Validate
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # 2) Save to a unique temp path
    tmp_name = f"{uuid.uuid4()}.pdf"
    tmp_path = os.path.join("/tmp", tmp_name)

    try:
        contents = await file.read()
        with open(tmp_path, "wb") as f:
            f.write(contents)

        # 3) Run pipeline: extract → clean → chunk
        raw_text   = extract_text(tmp_path)
        clean_text_ = clean_text(raw_text)
        passages   = chunk_text(clean_text_, max_tokens=200, overlap=20)

        # 4) Persist and generate flashcards
        doc_title = filename
        for idx, passage in enumerate(passages, start=1):
            # store the raw chunk for retrieval
            store_chunk(passage, doc_title)
            # generate a Q/A pair
            card = generate_flashcard(passage, source_id=f"{doc_title}#{idx}")
            # store the flashcard
            store_flashcard(
                question=card["question"],
                answer=card["answer"],
                source=card["source"],
                doc_title=doc_title
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "document": doc_title,
                "cards_generated": len(passages)
            }
        )

    except Exception as e:
        # Bubble up any pipeline errors
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Cleanup the temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
