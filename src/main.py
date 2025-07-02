from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.search import router as search_router
from api.flashcards import router as flashcards_router
from api.reviews import router as reviews_router
from api.documents import router as documents_router

app = FastAPI(title="Spaced-Repetition Tutor")

# CORS settings to allow frontend access (update as needed)
origins = [
    "https://spaced-repetition-tutor.vercel.app",  # Vercel production frontend
    "http://localhost:5173",  # Local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(search_router)
app.include_router(flashcards_router)
app.include_router(reviews_router)
app.include_router(documents_router)

# Root route (useful for testing on Render)
@app.get("/")
def root():
    return {"status": "Spaced Repetition Tutor backend is live!"}

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
