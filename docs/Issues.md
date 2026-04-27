##Issues

---

### Issue #1 — Create Project Repository Structure
**Labels:** `phase-1`
**Milestone:** Phase 1: Project Setup

```
Create the initial repository structure for backend and frontend.

**Tasks:**
- [x] Create backend folder
- [x] Create frontend folder
- [x] Create docs folder
- [x] Add PRD to docs
- [x] Setup basic README

**Deliverable:** Initial project skeleton.

**Status:** Completed.
```

---

### Issue #2 — Setup Backend API
**Labels:** `phase-1`, `backend`
**Milestone:** Phase 1: Project Setup

```
Implement a minimal backend API using FastAPI.

**Tasks:**
- [x] Create FastAPI application
- [x] Add basic `/analyze` endpoint
- [x] Setup request/response models

**Deliverable:** Running backend API that accepts a request.

**Status:** Completed.
```

---

### Issue #3 — Setup Frontend Interface
**Labels:** `phase-1`, `frontend`
**Milestone:** Phase 1: Project Setup

```
Create a minimal frontend interface.

**Tasks:**
- [x] Input field for decision question
- [x] Submit button
- [x] Result display area

**Deliverable:** User can send a decision question to the backend.

**Status:** Completed.
```

---

### Issue #4 — Implement Decision Parser (LLM)
**Labels:** `phase-2`, `backend`, `ai`
**Milestone:** Phase 2: Decision Engine

```
Implement LLM-based parsing of the decision question.

**Tasks:**
- [x] Send prompt to LLM
- [x] Extract decision options
- [x] Extract evaluation criteria
- [x] Return structured JSON

**Deliverable:** Function that converts user input into a structured decision representation.

**Example output:**
```json
{
  "options": ["London", "Berlin"],
  "criteria": ["Salary", "Career Opportunities", "Cost of Living"]
}
```

**Status:** Completed.
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

**Status:** Completed.
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

**Status:** Completed (`ParsedDecision`, `Criterion`, `Option` in `backend/decision.py`).
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

**Status:** Completed (`get_option_data` in `backend/services/criteria_data_service.py` + provider registry).
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

**Status:** Completed (`rank_options` in `backend/decision.py`; computes a true weighted average over criteria with data).
```

---

### Issue #9 — Normalize and Rank Options
**Labels:** `phase-3`, `backend`
**Milestone:** Phase 3: Data & Scoring

```
Normalize scores and rank decision options.

**Tasks:**
- [x] Normalize criteria values to a common scale
- [x] Compute final weighted score
- [x] Sort options by score descending

**Deliverable:** Ranked list of options.

**Status:** Completed (`min_max_normalize` in `backend/services/normalization.py` + `rank_options`).
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

**Status:** Completed (`generate_explanation` in `backend/services/llm_service.py`).
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

**Status:** Completed.
```

---

### Issue #12 — End-to-End Integration
**Labels:** `phase-4`, `backend`, `frontend`
**Milestone:** Phase 4: Explanation & UI

```
Connect all system components into a working pipeline.

**Tasks:**
- [x] Connect parser
- [x] Connect scoring model
- [x] Connect explanation generator
- [x] Test full end-to-end pipeline

**Deliverable:** Full working system.

**Status:** Completed (wired in `backend/main.py:analyze_decision`).
```

---

### Issue #13 — Add Score Visualization
**Labels:** `enhancement`, `frontend`

```
Add a simple visual comparison of option scores (bar chart).

**Deliverable:** Bar chart or visual score comparison in the results view.

**Status:** Completed (visual representation added; scores rendered as X/10).
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

**Status:** Partially addressed — prompt hardened against invented criteria; criterion/option name variance now tolerated via lowercase normalization and provider aliases.
```

---

### Issue #15 — Improve Error Handling
**Labels:** `enhancement`, `backend`, `frontend`

```
Handle edge cases gracefully throughout the system.

**Cases to handle:**
- [ ] Unclear or unparseable user input
- [ ] Missing decision options
- [x] Missing or unavailable data
- [ ] LLM API failures or timeouts
```

---

### Issue #16 — Replace Static Dataset with Pluggable Data Providers
**Labels:** `enhancement`, `backend`, `architecture`
**Milestone:** Phase 3: Data & Scoring

```
Replace the hardcoded city dataset with a pluggable provider architecture
so real data sources (World Bank, Open-Meteo, etc.) can serve criterion
values, with shared infrastructure for caching and normalization.

**Sub-issues:**
- [x] #16b — Refactor data layer into pluggable providers (`DataProvider`, `DataPoint`, direction).
- [x] #16c — Build a registry that routes criterion names to providers, with alias support for LLM name variance.
- [x] #16d — Add disk cache + `CachedProvider` wrapper for network-backed providers (TTL, negative-result caching).
- [x] #16e — Add Open-Meteo weather provider (geocode + comfort score from forecast).
- [x] #16f — Add World Bank salary provider (GDP-per-capita proxy) + shared geocoder.
- [ ] #16g — Replace `career_opportunities` and `cost_of_living` static stubs with real data sources (currently `StaticCityProvider`; see comment in `backend/services/providers/__init__.py`).
  - `career_opportunities`: candidates — World Bank unemployment-rate indicator (`SL.UEM.TOTL.ZS`, lower-is-better), or ILO/OECD employment-rate indicators. Country-level via the existing geocoder→ISO-3 path used by `WorldBankProvider`.
  - `cost_of_living`: candidates — World Bank PPP conversion factor (`PA.NUS.PPP`) or CPI inflation (`FP.CPI.TOTL.ZG`) as a proxy. True city-level cost-of-living needs a paid source (Numbeo/Expatistan); skip unless we want to introduce a key.
  - Both fit the existing `DataProvider` + `CachedProvider` pattern and the country-resolver from #16f, so implementation is mostly registration plumbing.

**Deliverable:** Default registry composes real providers behind cached wrappers; orchestrator unchanged.

**Status:** In progress — registry/cache/weather/salary infrastructure complete; #16g still pending.
```

---

### Issue #17 — Score Honestly with Missing Data
**Labels:** `enhancement`, `backend`

```
Make the ranking output truthful when data is incomplete or scores tie.

**Tasks:**
- [x] Compute weighted-average per option (sum(w·v) / sum(w) over criteria with data) so options aren't penalized for our gaps.
- [x] Track and surface `skipped_criteria` (criteria with no data for any option) on `ParsedDecision`.
- [x] Withhold `recommended_option` when the top score does not strictly beat the runner-up (no false confidence on ties).
- [x] Update explanation prompt to receive `skipped_criteria` and not invent a winner when no recommendation exists.

**Deliverable:** Ranking output honestly reflects data gaps and tie ambiguity.

**Status:** Completed.
```

---
