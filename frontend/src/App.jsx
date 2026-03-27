import { useState } from 'react'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

const CRITERION_LABELS = {
  raw_salary: 'Salary (raw)',
}

function toNiceCriterionLabel(key) {
  if (!key) return ''
  const small = new Set(['of', 'and', 'or', 'the', 'a', 'an', 'to', 'in', 'on', 'for'])
  const words = String(key).replace(/_/g, ' ').toLowerCase().split(' ')
  return words
    .map((w, i) => (i > 0 && small.has(w) ? w : w.charAt(0).toUpperCase() + w.slice(1)))
    .join(' ')
}

function criterionLabel(key) {
  return CRITERION_LABELS[key] ?? toNiceCriterionLabel(key)
}

function formatWeight(weight) {
  if (typeof weight !== 'number' || Number.isNaN(weight)) return ''
  // Backend currently returns weights like 0.5; older docs showed 40 (percent).
  const pct = weight <= 1 ? weight * 100 : weight
  return `${pct.toFixed(0)}%`
}

function formatNumber(n, digits = 3) {
  if (typeof n !== 'number' || Number.isNaN(n)) return ''
  return n.toFixed(digits).replace(/\.?0+$/, '')
}

async function analyzeDecision(question) {
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

  const criteria = results?.criteria ?? []
  const options = results?.options ?? []

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
              <h2 className="section-label">Question:</h2>
              <div className="card results-card">
                <div className="question-text">{results.question}</div>
                {results.recommended_option && (
                  <div className="recommended">
                    Recommended: <strong>{results.recommended_option}</strong>
                  </div>
                )}
              </div>
            </section>

            <section className="section">
              <h2 className="section-label">Extracted Criteria:</h2>
              <div className="criteria-grid">
                {criteria.map((criterion) => (
                  <div key={criterion.name} className="card criteria-card">
                    <div className="criteria-name">{criterionLabel(criterion.name)}</div>
                    <div className="criteria-weight">Weight: {formatWeight(criterion.weight)}</div>
                  </div>
                ))}
              </div>
            </section>

            <section className="section">
              <h2 className="section-label">Decision Results:</h2>
              <div className="card results-card">
                <div className="scores-row">
                  {options.map((option) => (
                    <div key={option.name} className="score-item">
                      <div className="option-name">{option.name}</div>
                      <div className="option-score">Score: {formatNumber(option.score, 4)}</div>
                    </div>
                  ))}
                </div>
                <div className="ranked-list">
                  {options.map((option, i) => (
                    <div key={option.name} className="rank-item">
                      {i + 1}. {option.name}
                    </div>
                  ))}
                </div>
              </div>
            </section>

            <section className="section">
              <h2 className="section-label">Per-criterion values:</h2>
              <div className="card results-card">
                <div className="table-wrap">
                  <table className="values-table">
                    <thead>
                      <tr>
                        <th>Option</th>
                        {criteria.map((c) => (
                          <th key={c.name}>{criterionLabel(c.name)}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {options.map((o) => (
                        <tr key={o.name}>
                          <td className="option-col">{o.name}</td>
                          {criteria.map((c) => (
                            <td key={c.name}>
                              {formatNumber(o.criterion_values?.[c.name], 4) || '—'}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </section>

            <section className="section">
              <h2 className="section-label">Explanation:</h2>
              <div className="card explanation-card">
                <p className="explanation-text">
                  {results.explanation ?? 'No explanation returned yet.'}
                </p>
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
