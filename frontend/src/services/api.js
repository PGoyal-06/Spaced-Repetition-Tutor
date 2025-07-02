// frontend/src/api.js
import axios from "axios";

// If VITE_API_URL is set (e.g. https://api.myapp.com), use that.
// Otherwise (in dev), leave blank so Vite's proxy kicks in.
const baseURL = import.meta.env.VITE_API_URL || "";

const api = axios.create({
  baseURL,
});

// Fetch next due flashcard
export function fetchNextReview(userId) {
  return api
    .get("/reviews/next", { params: { user_id: userId } })
    .then((r) => r.data);
}

// Submit a review
export function submitReview({ userId, flashcardId, quality }) {
  return api
    .post(`/reviews/${flashcardId}`, { user_id: userId, quality })
    .then((r) => r.data);
}

// Upload PDF & generate cards
export function uploadDocument(file) {
  const form = new FormData();
  form.append("file", file);
  return api
    .post("/documents/", form, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    .then((r) => r.data);
}

export default api;
