import os
import uuid
import traceback
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
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        return JSONResponse(status_code=400, content={"error": "Only PDF files are supported"})

    tmp_name = f"{uuid.uuid4()}.pdf"
    tmp_path = os.path.join("/tmp", tmp_name)

    try:
        contents = await file.read()
        with open(tmp_path, "wb") as f:
            f.write(contents)

        raw_text = extract_text(tmp_path)
        clean_text_ = clean_text(raw_text)
        passages = chunk_text(clean_text_, max_tokens=200, overlap=20)

        doc_title = filename
        for idx, passage in enumerate(passages, start=1):
            store_chunk(passage, doc_title)
            card = generate_flashcard(passage, source_id=f"{doc_title}#{idx}")
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
        print("❌ Error during document processing:")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": f"{type(e).__name__}: {str(e)}"}
        )

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
