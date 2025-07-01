import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/reviews':    'http://localhost:8000',
      '/flashcards': 'http://localhost:8000',
      '/search':     'http://localhost:8000',
      '/documents':  'http://localhost:8000',
    }
  }
})
