from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.search import router as search_router
from api.flashcards import router as flashcards_router
from api.reviews import router as reviews_router
from api.documents import router as documents_router

app = FastAPI(title="Spaced-Repetition Tutor")

# Frontend origins allowed to access this backend
origins = [
    "https://spaced-repetition-tutor.vercel.app",  # Production frontend on Vercel
    "http://localhost:5173",                       # Local frontend (Vite)
]

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(search_router)
app.include_router(flashcards_router)
app.include_router(reviews_router)
app.include_router(documents_router)

# Local development only
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
