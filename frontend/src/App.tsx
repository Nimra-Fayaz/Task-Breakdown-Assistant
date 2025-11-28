import { useState } from 'react'
import TaskInput from './components/TaskInput'
import GuideDisplay from './components/GuideDisplay'
import { TaskWithGuide } from './types'
import './App.css'

function App() {
  const [currentGuide, setCurrentGuide] = useState<TaskWithGuide | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleTaskSubmit = async (description: string) => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch('http://localhost:8000/api/tasks/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description }),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
        throw new Error(errorData.detail || `Server error: ${response.status}`)
      }

      const data = await response.json()
      setCurrentGuide(data)
    } catch (err) {
      if (err instanceof TypeError && err.message.includes('fetch')) {
        setError('Cannot connect to backend. Make sure the backend server is running on http://localhost:8000')
      } else {
        setError(err instanceof Error ? err.message : 'An error occurred')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <header className="app-header">
        <div className="container">
          <h1>🎯 Task Breakdown Assistant</h1>
          <p>Get detailed, beginner-friendly step-by-step guides for any task</p>
        </div>
      </header>

      <main className="container">
        <TaskInput onSubmit={handleTaskSubmit} loading={loading} />

        {error && (
          <div className="card" style={{ background: '#fee', border: '1px solid #fcc' }}>
            <p style={{ color: '#c33' }}>Error: {error}</p>
          </div>
        )}

        {loading && (
          <div className="card">
            <div className="loading">
              <div className="spinner"></div>
              <p>Generating your detailed guide... This may take a moment.</p>
            </div>
          </div>
        )}

        {currentGuide && !loading && (
          <GuideDisplay guide={currentGuide} />
        )}
      </main>
    </div>
  )
}

export default App
