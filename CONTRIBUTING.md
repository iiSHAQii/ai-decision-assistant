# Contributing to AI Decision Assistant

Thank you for contributing. Please read this document before opening issues or submitting pull requests.

---

## Table of Contents

- [Branching Strategy](#branching-strategy)
- [Commit Conventions](#commit-conventions)
- [Pull Request Rules](#pull-request-rules)
- [Issue Workflow](#issue-workflow)
- [Code Style](#code-style)

---

## Branching Strategy

We follow a simplified **Git Flow** model.

### Permanent Branches

| Branch | Purpose |
|---|---|
| `main` | Production-ready code only. Never commit directly. |
| `dev` | Integration branch. All features merge here first. |

### Working Branches

Branch from `dev`. Use the following naming conventions:

| Type | Pattern | Example |
|---|---|---|
| Feature | `feature/issue-{number}-short-description` | `feature/issue-4-decision-parser` |
| Bug fix | `fix/issue-{number}-short-description` | `fix/issue-9-score-normalization` |
| Docs | `docs/short-description` | `docs/update-contributing` |
| Refactor | `refactor/short-description` | `refactor/scoring-module` |

### Rules

- **Never push directly to `main` or `dev`.**
- Every feature branch must be tied to an open issue.
- Delete feature branches after they are merged.

---

## Commit Conventions

We use [Conventional Commits](https://www.conventionalcommits.org/).

### Format

```
<type>(<scope>): <short description>
```

### Types

| Type | When to use |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `refactor` | Code restructuring without behavior change |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks (deps, configs) |

### Examples

```
feat(parser): extract decision options from user input
fix(scoring): correct weight normalization for edge cases
docs(readme): add getting started section
```

---

## Pull Request Rules

### Before Opening a PR

- [ ] Your branch is up to date with `dev`
- [ ] The code runs locally without errors
- [ ] You have tested your changes manually
- [ ] The PR is linked to an issue (`Closes #<issue-number>`)

### PR Title Format

```
[#issue-number] Short description of change
```

Example: `[#4] Implement LLM-based decision parser`

### Review Process

- At least **1 approval** is required to merge into `dev`
- At least **1 approval** is required to merge `dev` into `main`
- The author should not merge their own PR unless it is a minor doc fix

---

## Issue Workflow

### Labels We Use

| Label | Meaning |
|---|---|
| `phase-1` `phase-2` `phase-3` `phase-4` | Which phase this belongs to |
| `backend` | Backend work |
| `frontend` | Frontend work |
| `ai` | LLM / prompt-related work |
| `bug` | Something is broken |
| `enhancement` | Optional improvement |
| `good first issue` | Good for onboarding |
| `blocked` | Cannot proceed, waiting on something |
| `in progress` | Actively being worked on |

### Picking Up an Issue

1. Comment on the issue: *"Taking this."*
2. Create a branch using the naming convention above.
3. Move the issue to **In Progress** on the project board.
4. Open a draft PR early if the work is substantial.

---

## Code Style

### Python (Backend)

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use type hints
- Docstrings on all functions

### JavaScript / React (Frontend)

- Use functional components
- Consistent naming: `camelCase` for variables, `PascalCase` for components
- Keep components small and focused

---

## Questions

Open a [Discussion](../../discussions) or ping the team directly.
