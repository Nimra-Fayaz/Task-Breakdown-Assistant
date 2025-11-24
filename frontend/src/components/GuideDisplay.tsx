import { useState, useEffect } from 'react'
import { TaskWithGuide, RatingStats } from '../types'

// Component to format instructions with bullet points and structure
function FormatInstructions({ instructions }: { instructions: string }) {
  // Split by newlines and format
  const formatText = (text: string) => {
    const lines = text.split('\n').filter(line => line.trim())
    const formatted: JSX.Element[] = []
    let currentList: string[] = []
    let listType: 'ordered' | 'unordered' | null = null

    const flushList = () => {
      if (currentList.length > 0) {
        if (listType === 'ordered') {
          formatted.push(
            <ol key={`list-${formatted.length}`} className="instruction-list">
              {currentList.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ol>
          )
        } else {
          formatted.push(
            <ul key={`list-${formatted.length}`} className="instruction-list">
              {currentList.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          )
        }
        currentList = []
        listType = null
      }
    }

    lines.forEach((line, index) => {
      const trimmed = line.trim()
      
      // Check if it's a numbered list item (1., 2., etc.)
      const numberedMatch = trimmed.match(/^(\d+)\.\s*(.+)$/)
      if (numberedMatch) {
        if (listType !== 'ordered') {
          flushList()
          listType = 'ordered'
        }
        currentList.push(numberedMatch[2])
        return
      }

      // Check if it's a bullet point (-, *, •)
      const bulletMatch = trimmed.match(/^[-*•]\s+(.+)$/)
      if (bulletMatch) {
        if (listType !== 'unordered') {
          flushList()
          listType = 'unordered'
        }
        currentList.push(bulletMatch[1])
        return
      }

      // Check if it's a command or code-like (starts with $, >, or contains backticks)
      if (trimmed.startsWith('$') || trimmed.startsWith('>') || trimmed.includes('`')) {
        flushList()
        formatted.push(
          <div key={`code-${index}`} className="instruction-command">
            {trimmed}
          </div>
        )
        return
      }

      // Regular paragraph
      if (trimmed) {
        flushList()
        // Check if it contains bold text (**text**)
        const parts = trimmed.split(/(\*\*[^*]+\*\*)/g)
        formatted.push(
          <p key={`para-${index}`} className="instruction-paragraph">
            {parts.map((part, i) => 
              part.startsWith('**') && part.endsWith('**') ? (
                <strong key={i}>{part.slice(2, -2)}</strong>
              ) : (
                part
              )
            )}
          </p>
        )
      }
    })

    flushList() // Flush any remaining list

    return formatted.length > 0 ? formatted : <p>{instructions}</p>
  }

  return <div className="formatted-instructions">{formatText(instructions)}</div>
}

interface GuideDisplayProps {
  guide: TaskWithGuide
}

function GuideDisplay({ guide }: GuideDisplayProps) {
  const [rating, setRating] = useState(0)
  const [hoveredRating, setHoveredRating] = useState(0)
  const [comment, setComment] = useState('')
  const [ratingStats, setRatingStats] = useState<RatingStats | null>(null)
  const [submittingRating, setSubmittingRating] = useState(false)

  useEffect(() => {
    // Fetch rating stats
    fetch(`http://localhost:8000/api/ratings/${guide.id}`)
      .then(res => res.json())
      .then(data => setRatingStats(data))
      .catch(err => console.error('Error fetching ratings:', err))
  }, [guide.id])

  const handleRatingSubmit = async () => {
    if (rating === 0) return

    setSubmittingRating(true)
    try {
      const response = await fetch('http://localhost:8000/api/ratings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          task_id: guide.id,
          rating,
          comment: comment.trim() || null,
        }),
      })

      if (response.ok) {
        // Consume response body (required by fetch API best practices)
        await response.json()
        // Refresh rating stats
        fetch(`http://localhost:8000/api/ratings/${guide.id}`)
          .then(res => res.json())
          .then(data => setRatingStats(data))
        
        setRating(0)
        setComment('')
        alert('Thank you for your rating!')
      }
    } catch (err) {
      console.error('Error submitting rating:', err)
    } finally {
      setSubmittingRating(false)
    }
  }

  const getComplexityStars = (score: number) => {
    return '⭐'.repeat(Math.min(score, 10))
  }

  return (
    <div>
      {/* Task Header */}
      <div className="card">
        <h2>{guide.title || 'Task Breakdown'}</h2>
        <p style={{ color: '#666', marginTop: '8px', marginBottom: '16px' }}>
          {guide.description}
        </p>
        
        <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
          <div>
            <strong>Complexity:</strong> {getComplexityStars(guide.complexity_score)} ({guide.complexity_score}/10)
          </div>
          {guide.estimated_total_time && (
            <div>
              <strong>Estimated Time:</strong> {Math.floor(guide.estimated_total_time / 60)}h {guide.estimated_total_time % 60}m
            </div>
          )}
          {ratingStats && ratingStats.total_ratings > 0 && (
            <div>
              <strong>Rating:</strong> {ratingStats.average_rating.toFixed(1)} ⭐ ({ratingStats.total_ratings} reviews)
            </div>
          )}
        </div>
      </div>

      {/* Guide Steps */}
      <div>
        <h2 style={{ marginBottom: '20px' }}>Step-by-Step Guide</h2>
        {guide.guide_steps
          .sort((a, b) => a.step_number - b.step_number)
          .map((step) => (
            <div key={step.id} className="step-card">
              <div className="step-header">
                <div style={{ display: 'flex', alignItems: 'center', flex: 1 }}>
                  <div className="step-number">{step.step_number}</div>
                  <div className="step-title">{step.title}</div>
                </div>
                {step.estimated_time && (
                  <div className="step-time">⏱️ {step.estimated_time} min</div>
                )}
              </div>

              <div className="step-description">{step.description}</div>

              {step.detailed_instructions && (
                <div className="detailed-instructions">
                  <FormatInstructions instructions={step.detailed_instructions} />
                </div>
              )}

              {step.code_snippets && step.code_snippets.length > 0 && (
                <div>
                  {step.code_snippets.map((snippet, idx) => (
                    <div key={idx} className="code-snippet">
                      {snippet}
                    </div>
                  ))}
                </div>
              )}

              {step.resources && step.resources.length > 0 && (
                <div style={{ marginTop: '12px' }}>
                  <strong>📚 Resources:</strong>
                  <ul style={{ marginLeft: '20px', marginTop: '8px' }}>
                    {step.resources.map((resource, idx) => (
                      <li key={idx}>
                        <a href={resource} target="_blank" rel="noopener noreferrer">
                          {resource}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {step.dependencies && step.dependencies.length > 0 && (
                <div style={{ marginTop: '12px', color: '#666' }}>
                  ⚠️ <strong>Depends on:</strong> Steps {step.dependencies.join(', ')}
                </div>
              )}

              {step.tips && (
                <div className="tip-box">
                  💡 <strong>Tip:</strong> {step.tips}
                </div>
              )}

              {step.warnings && (
                <div className="warning-box">
                  ⚠️ <strong>Warning:</strong> {step.warnings}
                </div>
              )}

              {step.verification_steps && (
                <div style={{ marginTop: '12px', padding: '12px', background: '#e8f5e9', borderRadius: '4px' }}>
                  ✅ <strong>Verify:</strong> {step.verification_steps}
                </div>
              )}
            </div>
          ))}
      </div>

      {/* Rating Section */}
      <div className="card">
        <h3>Rate This Guide</h3>
        <div className="rating-section">
          <div style={{ display: 'flex', gap: '4px' }}>
            {[1, 2, 3, 4, 5].map((star) => (
              <span
                key={star}
                className={`star ${star <= (hoveredRating || rating) ? 'active' : ''}`}
                onClick={() => setRating(star)}
                onMouseEnter={() => setHoveredRating(star)}
                onMouseLeave={() => setHoveredRating(0)}
              >
                ★
              </span>
            ))}
          </div>
          <input
            type="text"
            placeholder="Optional comment..."
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            style={{ flex: 1, padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
          />
          <button
            className="btn btn-primary"
            onClick={handleRatingSubmit}
            disabled={rating === 0 || submittingRating}
          >
            {submittingRating ? 'Submitting...' : 'Submit Rating'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default GuideDisplay

