import { useState } from 'react'
import './App.css'

// Set to false when backend API is ready
const USE_MOCK_API = true
const API_BASE_URL = 'http://localhost:8000'

const MOCK_RESULT = {
  criteria: [
    { name: 'Salary', weight: 40 },
    { name: 'Career Opportunities', weight: 40 },
    { name: 'Cost of Living', weight: 20 },
  ],
  options: [
    { name: 'London', score: 7.5 },
    { name: 'Berlin', score: 6.2 },
  ],
  explanation:
    'London is recommended due to higher average salaries and better career opportunities, despite the higher cost of living.',
}

async function analyzeDecision(question) {
  if (USE_MOCK_API) {
    await new Promise((r) => setTimeout(r, 800))
    return MOCK_RESULT
  }

  const response = await fetch(`${API_BASE_URL}/api/decisions/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question: question.trim() }),
  })

  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: response.statusText }))
    throw new Error(err.detail || `Request failed: ${response.status}`)
  }

  return response.json()
}

function App() {
  const [question, setQuestion] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const handleAnalyze = async () => {
    if (!question.trim()) return
    setIsAnalyzing(true)
    setResults(null)
    setError(null)

    try {
      const data = await analyzeDecision(question)
      setResults(data)
    } catch (err) {
      setError(err.message || 'Something went wrong')
      console.error(err)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleNewDecision = () => {
    setQuestion('')
    setResults(null)
    setError(null)
  }

  return (
    <div className="app">
      <header className="header">
        <h1>AI Decision Assistant</h1>
      </header>

      <main className="main">
        <section className="section input-section">
          <div className="input-row">
            <label htmlFor="question" className="input-label">
              Enter your decision question:
            </label>
            <textarea
              id="question"
              className="question-input"
              placeholder="Should I move to London or Berlin? Salary and career opportunities are important to me."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              disabled={isAnalyzing}
              rows={3}
            />
            <button
              className="btn btn-primary"
              onClick={handleAnalyze}
              disabled={isAnalyzing || !question.trim()}
            >
              {isAnalyzing ? 'Analyzing…' : 'Analyze'}
            </button>
          </div>
        </section>

        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}

        {results && (
          <>
            <section className="section">
              <h2 className="section-label">Extracted Criteria:</h2>
              <div className="criteria-grid">
                {results.criteria.map((criterion) => (
                  <div key={criterion.name} className="card criteria-card">
                    <div className="criteria-name">{criterion.name}</div>
                    <div className="criteria-weight">Weight: {criterion.weight}%</div>
                  </div>
                ))}
              </div>
            </section>

            <section className="section">
              <h2 className="section-label">Decision Results:</h2>
              <div className="card results-card">
                <div className="scores-row">
                  {results.options.map((option) => (
                    <div key={option.name} className="score-item">
                      <div className="option-name">{option.name}</div>
                      <div className="option-score">Score: {option.score}</div>
                    </div>
                  ))}
                </div>
                <div className="ranked-list">
                  {results.options.map((option, i) => (
                    <div key={option.name} className="rank-item">
                      {i + 1}. {option.name}
                    </div>
                  ))}
                </div>
              </div>
            </section>

            <section className="section">
              <h2 className="section-label">Explanation:</h2>
              <div className="card explanation-card">
                <p className="explanation-text">{results.explanation}</p>
              </div>
            </section>

            <div className="actions">
              <button className="btn btn-primary" onClick={handleNewDecision}>
                Start New Decision
              </button>
            </div>
          </>
        )}
      </main>
    </div>
  )
}

export default App
