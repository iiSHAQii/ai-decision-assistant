# GitHub Setup Guide — AI Decision Assistant

Follow these steps exactly, in order.

---

## STEP 1 — Create the Repository

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `ai-decision-assistant`
   - **Description:** `AI-powered tool that helps users structure and evaluate complex decisions using natural language.`
   - **Visibility:** Public
   - ❌ Do NOT initialize with README (you already have the files)
3. Click **Create repository**

---

## STEP 2 — Push the Files

Open your terminal in the folder you extracted from this zip, then run:

```bash
git init
git add .
git commit -m "chore: initial project structure"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-decision-assistant.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## STEP 3 — Create the `dev` Branch

```bash
git checkout -b dev
git push -u origin dev
```

---

## STEP 4 — Protect Branches

1. Go to your repo → **Settings** → **Branches**
2. Click **Add branch protection rule**

**For `main`:**
- Branch name pattern: `main`
- ✅ Require a pull request before merging
- ✅ Require at least 1 approval
- ✅ Do not allow bypassing the above settings
- Click **Create**

**For `dev`:**
- Branch name pattern: `dev`
- ✅ Require a pull request before merging
- ✅ Require at least 1 approval
- Click **Create**

---

## STEP 5 — Add Collaborator (Hypnos8)

1. Go to **Settings** → **Collaborators**
2. Click **Add people**
3. Search: `Hypnos8`
4. Select role: **Write**
5. Click **Add Hypnos8 to this repository**

He will receive an email invite.

---

## STEP 6 — Create Labels

Go to your repo → **Issues** → **Labels** → **New label**

Create these labels (copy name and color exactly):

| Label Name | Color |
|---|---|
| `phase-1` | `#0075ca` |
| `phase-2` | `#e4e669` |
| `phase-3` | `#d93f0b` |
| `phase-4` | `#0e8a16` |
| `backend` | `#5319e7` |
| `frontend` | `#f9d0c4` |
| `ai` | `#c5def5` |
| `blocked` | `#b60205` |
| `in progress` | `#fbca04` |
| `good first issue` | `#7057ff` |

---

## STEP 7 — Create Milestones

Go to **Issues** → **Milestones** → **New milestone**

Create these 4 milestones:

1. **Phase 1: Project Setup**
2. **Phase 2: Decision Engine**
3. **Phase 3: Data & Scoring**
4. **Phase 4: Explanation & UI**

No due dates needed unless you want them.

---

## STEP 8 — Create Issues

Go to **Issues** → **New issue** and create all 15 issues below.
For each one: paste the title and body, assign the correct labels and milestone, then submit.

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

## STEP 9 — Set Up the Project Board

1. Go to your repo → **Projects** → **New project**
2. Choose **Board** view
3. Name it: `AI Decision Assistant`
4. Create these columns:
   - **Backlog**
   - **In Progress**
   - **In Review**
   - **Done**
5. Drag all issues into **Backlog** to start

---

## STEP 10 — Set Default Branch

1. Go to **Settings** → **General**
2. Under **Default branch**, change it to `dev`
3. This means all PRs default to targeting `dev`

---

## You're Done.

When you or Hypnos8 want to work on something:
1. Pick an issue from the board
2. Move it to **In Progress**
3. Create a branch: `feature/issue-N-description`
4. Do the work
5. Open a PR targeting `dev`
6. Get 1 approval, merge
