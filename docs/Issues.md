##Issues

---

### Issue #1 — Create Project Repository Structure
**Labels:** `phase-1`
**Milestone:** Phase 1: Project Setup

```
Create the initial repository structure for backend and frontend.

**Tasks:**
- [ ] Create backend folder
- [ ] Create frontend folder
- [ ] Create docs folder
- [ ] Add PRD to docs
- [ ] Setup basic README

**Deliverable:** Initial project skeleton.
```

---

### Issue #2 — Setup Backend API
**Labels:** `phase-1`, `backend`
**Milestone:** Phase 1: Project Setup

```
Implement a minimal backend API using FastAPI.

**Tasks:**
- [ ] Create FastAPI application
- [ ] Add basic `/analyze` endpoint
- [ ] Setup request/response models

**Deliverable:** Running backend API that accepts a request.
```

---

### Issue #3 — Setup Frontend Interface
**Labels:** `phase-1`, `frontend`
**Milestone:** Phase 1: Project Setup

```
Create a minimal frontend interface.

**Tasks:**
- [ ] Input field for decision question
- [ ] Submit button
- [ ] Result display area

**Deliverable:** User can send a decision question to the backend.
```

---

### Issue #4 — Implement Decision Parser (LLM)
**Labels:** `phase-2`, `backend`, `ai`
**Milestone:** Phase 2: Decision Engine

```
Implement LLM-based parsing of the decision question.

**Tasks:**
- [ ] Send prompt to LLM
- [ ] Extract decision options
- [ ] Extract evaluation criteria
- [ ] Return structured JSON

**Deliverable:** Function that converts user input into a structured decision representation.

**Example output:**
```json
{
  "options": ["London", "Berlin"],
  "criteria": ["Salary", "Career Opportunities", "Cost of Living"]
}
```
```

---

### Issue #5 — Implement Criteria Weight Extraction
**Labels:** `phase-2`, `backend`, `ai`
**Milestone:** Phase 2: Decision Engine

```
Extend the parser to estimate the relative importance of criteria.

**Deliverable:** Criteria with associated weights.

**Example output:**
```
Salary: 0.4
Career Opportunities: 0.4
Cost of Living: 0.2
```
```

---

### Issue #6 — Create Decision Data Structure
**Labels:** `phase-2`, `backend`
**Milestone:** Phase 2: Decision Engine

```
Define the internal representation of a decision.

**Deliverable:** Reusable decision object.

**Example structure:**
```python
Decision:
  options: []
  criteria: []
  weights: {}
```
```

---

### Issue #7 — Implement Data Retrieval Module
**Labels:** `phase-3`, `backend`
**Milestone:** Phase 3: Data & Scoring

```
Create a module that retrieves relevant information for each decision option.

**Examples of data:**
- Average salary
- Cost of living index
- Other relevant indicators

For MVP, this can use static data or simple API calls.

**Deliverable:** Function returning comparable data for each option.
```

---

### Issue #8 — Implement Decision Scoring Model
**Labels:** `phase-3`, `backend`
**Milestone:** Phase 3: Data & Scoring

```
Implement a weighted scoring algorithm for each option.

**Formula:**
```
score(option) =
  weight_salary * salary_score +
  weight_career * career_score -
  weight_cost * cost_score
```

**Deliverable:** Function returning a score for each option.
```

---

### Issue #9 — Normalize and Rank Options
**Labels:** `phase-3`, `backend`
**Milestone:** Phase 3: Data & Scoring

```
Normalize scores and rank decision options.

**Tasks:**
- [ ] Normalize criteria values to a common scale
- [ ] Compute final weighted score
- [ ] Sort options by score descending

**Deliverable:** Ranked list of options.
```

---

### Issue #10 — Generate Decision Explanation
**Labels:** `phase-4`, `backend`, `ai`
**Milestone:** Phase 4: Explanation & UI

```
Use the LLM to generate a human-readable explanation of the result.

**Input:**
- Options
- Criteria and weights
- Scores

**Output:**
Natural language explanation of the recommendation.

**Deliverable:** Explanation text returned by backend.
```

---

### Issue #11 — Display Results in Frontend
**Labels:** `phase-4`, `frontend`
**Milestone:** Phase 4: Explanation & UI

```
Show decision results in the UI.

**Display:**
- Compared options with scores
- Criteria and weights
- Ranked list
- Recommendation explanation

**Deliverable:** User can see structured results in the interface.
```

---

### Issue #12 — End-to-End Integration
**Labels:** `phase-4`, `backend`, `frontend`
**Milestone:** Phase 4: Explanation & UI

```
Connect all system components into a working pipeline.

**Tasks:**
- [ ] Connect parser
- [ ] Connect scoring model
- [ ] Connect explanation generator
- [ ] Test full end-to-end pipeline

**Deliverable:** Full working system.
```

---

### Issue #13 — Add Score Visualization
**Labels:** `enhancement`, `frontend`

```
Add a simple visual comparison of option scores (bar chart).

**Deliverable:** Bar chart or visual score comparison in the results view.
```

---

### Issue #14 — Improve Prompt Engineering
**Labels:** `enhancement`, `ai`

```
Refine LLM prompts to improve parsing accuracy and explanation quality.

**Areas to improve:**
- Option extraction from ambiguous inputs
- Weight assignment consistency
- Explanation tone and clarity
```

---

### Issue #15 — Improve Error Handling
**Labels:** `enhancement`, `backend`, `frontend`

```
Handle edge cases gracefully throughout the system.

**Cases to handle:**
- [ ] Unclear or unparseable user input
- [ ] Missing decision options
- [ ] Missing or unavailable data
- [ ] LLM API failures or timeouts
```

---
