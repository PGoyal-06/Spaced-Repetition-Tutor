from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
import logging

from ingest.extractor import extract_text
from ingest.cleaner import clean_text
from ingest.chunker import chunk_text
from ingest.storage import store_chunk, store_flashcard, generate_flashcard

router = APIRouter(prefix="/documents", tags=["documents"])
logger = logging.getLogger("uvicorn.error")

@router.post("/", summary="Upload a lecture PDF and generate flashcards")
async def upload_and_generate(file: UploadFile = File(...)):
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    tmp_name = f"{uuid.uuid4()}.pdf"
    tmp_path = os.path.join("/tmp", tmp_name)

    # Core processing (exceptions bubble to global handler)
    contents = await file.read()
    logger.info(f"✅ File read successfully: {len(contents)} bytes")

    with open(tmp_path, "wb") as f:
        f.write(contents)
    logger.info(f"✅ File written to: {tmp_path}")

    raw_text = extract_text(tmp_path)
    logger.info(f"✅ Extracted text length: {len(raw_text)}")

    clean_text_ = clean_text(raw_text)
    passages = chunk_text(clean_text_, max_tokens=200, overlap=20)
    logger.info(f"✅ Chunked into {len(passages)} passages")

    doc_title = filename
    for idx, passage in enumerate(passages, start=1):
        store_chunk(passage, doc_title)
        logger.info(f"✅ Stored chunk #{idx}")

        card = generate_flashcard(passage, source_id=f"{doc_title}#{idx}")
        logger.info(f"✅ Flashcard generated for chunk #{idx}")

        store_flashcard(
            question=card["question"],
            answer=card["answer"],
            source=card["source"],
            doc_title=doc_title
        )
        logger.info(f"✅ Flashcard stored for chunk #{idx}")

    # Clean up temp file
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
        logger.info(f"🧹 Temp file deleted: {tmp_path}")

    return JSONResponse(
        status_code=200,
        content={"status": "ok", "document": doc_title, "cards_generated": len(passages)}
    )
