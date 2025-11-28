import { useState } from 'react'

interface TaskInputProps {
  onSubmit: (description: string) => void
  loading: boolean
}

function TaskInput({ onSubmit, loading }: TaskInputProps) {
  const [description, setDescription] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (description.trim().length >= 10) {
      onSubmit(description.trim())
    }
  }

  return (
    <div className="card">
      <h2>📝 Enter Your Task or Assignment</h2>
      <p style={{ color: '#666', marginBottom: '20px' }}>
        Describe the task, assignment, or project you need help with. Our AI will break it down into detailed, beginner-friendly steps.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="task-description">Task Description</label>
          <textarea
            id="task-description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Example: Build a web application with user authentication. The app should allow users to register, login, and access a dashboard..."
            disabled={loading}
            required
            minLength={10}
          />
          <small style={{ color: '#666', marginTop: '8px', display: 'block' }}>
            Minimum 10 characters. Be as detailed as possible for better results.
          </small>
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={loading || description.trim().length < 10}
        >
          {loading ? 'Generating Guide...' : 'Generate Step-by-Step Guide'}
        </button>
      </form>
    </div>
  )
}

export default TaskInput
