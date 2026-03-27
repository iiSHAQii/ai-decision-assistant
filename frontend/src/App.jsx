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

function formatScore(score) {
  if (typeof score !== 'number' || Number.isNaN(score)) return '—'
  // Convert from [0, 1] range to /10 scale
  const scoreOutOfTen = score * 10
  return `${formatNumber(scoreOutOfTen, 1)}/10`
}

function formatCriterionValue(value) {
  if (typeof value !== 'number' || Number.isNaN(value)) return '—'
  // Convert from [0, 1] range to /10 scale
  const valueOutOfTen = value * 10
  return formatNumber(valueOutOfTen, 1)
}

function formatDelta(delta) {
  if (typeof delta !== 'number' || Number.isNaN(delta)) return '—'
  // Convert from [0, 1] range to /10 scale
  const deltaOutOfTen = delta * 10
  return formatNumber(deltaOutOfTen, 1)
}

function buildLeaderboard(options, recommendedOption) {
  const safeOptions = Array.isArray(options) ? options : []
  const scored = safeOptions
    .map((o, idx) => ({
      idx,
      name: o?.name ?? `Option ${idx + 1}`,
      score: typeof o?.score === 'number' && !Number.isNaN(o.score) ? o.score : null,
    }))
    .filter((o) => o.name)

  const bestScore = scored.reduce((acc, o) => (o.score == null ? acc : Math.max(acc, o.score)), 0)

  return scored.map((o, rankIdx) => {
    // All scores are normalized to [0, 1] range, so percentage is simply score * 100
    const scorePct = o.score == null ? 0 : Math.min(100, Math.max(0, o.score * 100))

    const deltaVsBest = o.score == null ? null : bestScore - o.score
    const isRecommended = recommendedOption != null && o.name === recommendedOption

    return {
      ...o,
      rank: rankIdx + 1,
      bestScore,
      scorePct,
      deltaVsBest,
      isRecommended,
    }
  })
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
  const leaderboard = buildLeaderboard(options, results?.recommended_option)

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
                <div className="leaderboard" role="list">
                  {leaderboard.map((o) => (
                    <div
                      key={o.name}
                      className={`leaderboard-row${o.rank === 1 ? ' winner' : ''}`}
                      role="listitem"
                    >
                      <div className="leaderboard-left">
                        <div className="rank-badge" aria-label={`Rank ${o.rank}`}>
                          {o.rank}
                        </div>
                        <div className="leaderboard-name">
                          <div className="option-name-row">
                            <span className="option-name">{o.name}</span>
                            {o.isRecommended && <span className="recommended-badge">Recommended</span>}
                          </div>
                          <div className="score-meta">
                            <span className="option-score">
                              Score: {formatScore(o.score)}
                            </span>
                            {o.rank !== 1 && o.deltaVsBest != null && (
                              <span className="delta">
                                −{formatDelta(o.deltaVsBest)} vs best
                              </span>
                            )}
                          </div>
                        </div>
                      </div>

                      <div className="leaderboard-right">
                        <div className="score-bar-track" aria-hidden="true">
                          <div className="score-bar-fill" style={{ width: `${o.scorePct}%` }} />
                        </div>
                        <div className="score-bar-text">{formatScore(o.score)}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </section>

            <section className="section">
              <h2 className="section-label">Per-criterion values:</h2>
              <p className="scale-info">All criterion values are scored on a scale of 0-10</p>
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
                              {formatCriterionValue(o.criterion_values?.[c.name])}
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
