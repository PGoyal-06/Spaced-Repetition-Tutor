import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'

// Custom plugin to copy _redirects after build
function copyRedirects() {
  return {
    name: 'copy-redirects',
    closeBundle() {
      const src = 'public/_redirects'
      const dest = 'dist/_redirects'
      if (fs.existsSync(src)) {
        fs.copyFileSync(src, dest)
        console.log(`✅ Copied _redirects to ${dest}`)
      } else {
        console.warn(`⚠️ _redirects file not found at ${src}`)
      }
    }
  }
}

export default defineConfig({
  plugins: [react(), copyRedirects()],
  server: {
    proxy: {
      '/reviews':    'http://localhost:8000',
      '/flashcards': 'http://localhost:8000',
      '/search':     'http://localhost:8000',
      '/documents':  'http://localhost:8000',
    }
  }
})
