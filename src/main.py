import traceback
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from db.session import engine, init_db, Base
from api.search import router as search_router
from api.flashcards import router as flashcards_router
from api.reviews import router as reviews_router
from api.documents import router as documents_router

# Initialize FastAPI with debug (disable in prod later)
app = FastAPI(title="Spaced-Repetition Tutor", debug=True)

# Global exception handler to reveal full tracebacks
@app.exception_handler(Exception)
async def reveal_all_exceptions(request: Request, exc: Exception):
    tb = traceback.format_exc()
    print(tb, file=sys.stderr)
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "traceback": tb.splitlines()
        },
    )

# Create tables at startup
@app.on_event("startup")
def on_startup():
    # Initialize DB schema
    init_db()

# CORS settings
origins = [
    "https://spaced-repetition-tutor.vercel.app",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(search_router)
app.include_router(flashcards_router)
app.include_router(reviews_router)
app.include_router(documents_router)

# Root endpoint
@app.get("/")
def root():
    return {"status": "Spaced Repetition Tutor backend is live!"}

# Local dev entrypoint
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
    