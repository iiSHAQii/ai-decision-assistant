# 🧠 AI Decision Assistant

> A web-based tool that helps users structure and evaluate complex decisions using natural language and AI.

[![Status](https://img.shields.io/badge/status-in%20development-yellow)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)

---

## What It Does

Users describe a decision in plain text — for example:

> *"Should I move to London or Berlin? Salary and career opportunities are important to me."*

The system then:
1. Extracts decision options and evaluation criteria
2. Assigns weights to each criterion
3. Gathers relevant data per option
4. Computes a transparent weighted score
5. Generates a clear natural-language explanation

---

## Example Output

**Input:**
```
Should I move to London or Berlin? Salary and career opportunities matter most, but cost of living is also important.
```

**Extracted Structure:**

| Criterion | Weight |
|---|---|
| Salary | 40% |
| Career Opportunities | 40% |
| Cost of Living | 20% |

**Result:**

| Option | Score |
|---|---|
| 🥇 London | 7.5 |
| 🥈 Berlin | 6.2 |

> London scores higher due to stronger career opportunities and higher average salaries, despite the higher cost of living.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| AI | Claude / GPT-4o mini |
| Frontend | React |
| Data | APIs + static datasets |

---

## Project Structure

```
ai-decision-assistant/
├── backend/          # FastAPI application
├── frontend/         # React UI
├── docs/             # PRD, requirements, architecture
└── .github/          # Issue templates, PR template, workflows
```

---

## Getting Started

> Setup instructions will be added as the project progresses.

---

## Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening issues or pull requests.

---

## Roadmap

See the [Issues tab](../../issues) for the full breakdown of phases and tasks.

Phases:
- **Phase 1** — Project Setup
- **Phase 2** — Decision Engine
- **Phase 3** — Data & Scoring
- **Phase 4** — Explanation & UI

---

## Team

| Name | Role |
|---|---|
| Ishaq | Co-Lead |
| [Hypnos8](https://github.com/Hypnos8) | Lead |
