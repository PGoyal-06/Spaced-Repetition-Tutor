// frontend/src/api.js
import axios from 'axios'

// Create an axios instance that uses the current origin (so Vite proxy applies)
const api = axios.create({
  baseURL: ''
});

/**
 * Fetch the next due flashcard for a user
 */
export function fetchNextReview(userId) {
  return api
    .get('/reviews/next', { params: { user_id: userId } })
    .then(res => res.data)
}

/**
 * Submit a review rating and advance the schedule
 * Expects an object: { userId, flashcardId, quality }
 */
export function submitReview({ userId, flashcardId, quality }) {
  return api
    .post(`/reviews/${flashcardId}`, { user_id: userId, quality })
    .then(res => res.data)
}

/**
 * Upload a PDF lecture and trigger flashcard generation
 */
export function uploadDocument(file) {
  const form = new FormData()
  form.append('file', file)
  return api
    .post('/documents/', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    .then(res => res.data)
}

export default api;
