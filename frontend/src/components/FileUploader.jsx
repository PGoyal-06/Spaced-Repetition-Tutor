import React, { useState } from 'react'
import api from '../services/api'

export default function FileUploader({ onComplete, onDone }) {
  const [selected, setSelected] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleUpload = async () => {
    if (!selected) return
    setLoading(true)
    const form = new FormData()
    form.append('file', selected)
    try {
      await api.post('/documents/', form, { headers: { 'Content-Type': 'multipart/form-data' } })
      if (onComplete) onComplete()
      else if (onDone) onDone()
    } catch (err) {
      console.error(err.response.data)
      alert('Upload failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <label className="block text-sm text-white/90 font-medium tracking-wide">
        Upload your lecture PDF
        <input
          type="file"
          accept="application/pdf"
          onChange={e => setSelected(e.target.files[0])}
          className="mt-2 block w-full text-sm text-white/80 file:mr-4 file:py-2 file:px-5 file:rounded-lg file:border-0 file:font-semibold file:bg-indigo-500 file:text-white hover:file:bg-indigo-600 transition duration-150"
        />
      </label>

      <button
        onClick={handleUpload}
        disabled={!selected || loading}
        className={`w-full py-3 rounded-xl text-lg font-semibold transition-all duration-200 shadow-md ${
          loading || !selected
            ? 'bg-indigo-300 cursor-not-allowed'
            : 'bg-indigo-600 hover:bg-indigo-700'
        }`}
      >
        {loading ? 'Processing...' : 'Upload & Generate Cards'}
      </button>
    </div>
  )
}
