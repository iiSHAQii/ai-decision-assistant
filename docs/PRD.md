# Product Requirements Document — AI Decision Assistant

**Version:** 1.0  
**Status:** Draft  

---

## 1. Overview

**AI Decision Assistant** is a web-based tool that helps users structure and evaluate complex decisions using natural language.

Users describe a decision problem in plain text. The system extracts decision options and evaluation criteria, gathers relevant information, computes a weighted score for each option, and provides a transparent recommendation.

**Goal:** Demonstrate how LLMs can help structure decisions while keeping the final evaluation transparent and explainable.

---

## 2. Problem Statement

Many real-world decisions involve balancing multiple competing factors — cost, salary, lifestyle, or opportunities. People often struggle to:

- Structure the decision clearly
- Identify all relevant criteria
- Compare options objectively without bias

As a result, decision-making becomes slow, emotional, and hard to explain to others.

---

## 3. Proposed Solution

Four-step process:

1. **User Input** — User describes a decision in natural language.
2. **Decision Structuring (LLM)** — System extracts options, criteria, and relative weights.
3. **Information Gathering** — System collects relevant data per option.
4. **Scoring & Explanation** — Weighted model scores each option; LLM generates explanation.

---

## 4. Example Scenario

**Input:**
> "Should I move to London or Berlin? Salary and career opportunities matter most, but cost of living is also important."

**Extracted Structure:**

| Option | — |
|---|---|
| London | ✓ |
| Berlin | ✓ |

| Criterion | Weight |
|---|---|
| Salary | 40% |
| Career Opportunities | 40% |
| Cost of Living | 20% |

**Recommendation:**
> London receives a higher score mainly due to stronger career opportunities and higher salaries, despite higher living costs.

---

## 5. User Stories

- As a user, I want to describe a decision in natural language so I don't need to define criteria manually.
- As a user, I want the system to structure the decision for me so I can understand the factors involved.
- As a user, I want a clear explanation of the recommendation so I can trust the result.

---

## 6. MVP Scope

**In scope:**
- Natural language decision input
- LLM-based option and criteria extraction
- Comparison of 2–3 options
- Weighted scoring model
- Explanation generation
- Basic web interface

**Out of scope (for MVP):**
- User accounts or authentication
- Persistent decision history
- Advanced ML models
- Multi-agent systems
- Mobile applications

---

## 7. System Architecture

```
Frontend (React)
      │
      ▼
Backend API (FastAPI)
      │
      ▼
Decision Engine
  ├── LLM Parser
  ├── Data Retrieval Module
  ├── Scoring Model
  └── Explanation Generator
```

---

## 8. Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, FastAPI |
| AI | Claude API / GPT-4o mini |
| Frontend | React |
| Data | Static datasets + optional APIs |

---

## 9. Success Criteria

The project is successful if:
- Users can input a decision question in plain language
- The system extracts meaningful options and criteria
- The system produces a structured, scored recommendation
- The explanation is understandable and references actual criteria
