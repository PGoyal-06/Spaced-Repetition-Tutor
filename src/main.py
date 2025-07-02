from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.search import router as search_router
from api.flashcards import router as flashcards_router
from api.reviews import router as reviews_router
from api.documents import router as documents_router

app = FastAPI(title="Spaced-Repetition Tutor")

# Replace this with your actual Vercel frontend URL
origins = [
    "https://spaced-repetition-tutor.vercel.app/",  # For production on Vercel
    "http://localhost:5173",  # For local dev with Vite
]

# Enable CORS so your frontend can call your backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all (less secure)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API routers
app.include_router(search_router)
app.include_router(flashcards_router)
app.include_router(reviews_router)
app.include_router(documents_router)

# Optional for local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
