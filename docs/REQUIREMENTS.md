# Requirements — AI Decision Assistant

## Table of Contents

- [Functional Requirements](#functional-requirements)
- [Non-Functional Requirements](#non-functional-requirements)

---

## Functional Requirements

Functional requirements define **what the system must do**.

---

### FR-1: Decision Input

| ID | Requirement |
|---|---|
| FR-1.1 | The system shall allow users to enter a decision question in natural language. |
| FR-1.2 | The input shall support questions comparing two or more options. |
| FR-1.3 | The user shall be able to submit the decision question through a web interface. |

---

### FR-2: Decision Parsing

| ID | Requirement |
|---|---|
| FR-2.1 | The system shall extract decision options from the user input using an LLM. |
| FR-2.2 | The system shall extract evaluation criteria mentioned in the input. |
| FR-2.3 | The system shall assign relative importance (weights) to the extracted criteria. |

---

### FR-3: Structured Decision Representation

| ID | Requirement |
|---|---|
| FR-3.1 | The system shall convert the parsed decision into a structured format containing options, criteria, and weights. |
| FR-3.2 | The structured representation shall be used as input for all downstream processing. |

---

### FR-4: Information Retrieval

| ID | Requirement |
|---|---|
| FR-4.1 | The system shall gather relevant information for each decision option. |
| FR-4.2 | Retrieved data may include salary, cost of living, or other indicators relevant to the criteria. |
| FR-4.3 | The system shall normalize retrieved data to enable fair comparison. |

---

### FR-5: Decision Scoring

| ID | Requirement |
|---|---|
| FR-5.1 | The system shall compute a score for each decision option using a weighted scoring model. |
| FR-5.2 | Each evaluation criterion shall contribute to the final score based on its assigned weight. |
| FR-5.3 | The system shall rank options based on their computed scores. |

---

### FR-6: Recommendation Generation

| ID | Requirement |
|---|---|
| FR-6.1 | The system shall generate a recommendation based on the highest-scoring option. |
| FR-6.2 | The system shall present a ranked list of options to the user. |

---

### FR-7: Explanation Generation

| ID | Requirement |
|---|---|
| FR-7.1 | The system shall generate a natural language explanation of why the top option scored highest. |
| FR-7.2 | The explanation shall reference the most influential evaluation criteria. |

---

### FR-8: Results Display

| ID | Requirement |
|---|---|
| FR-8.1 | The system shall display decision results in the web interface. |
| FR-8.2 | The interface shall show compared options, evaluation criteria, final scores, and the explanation. |

---

### FR-9: Error Handling

| ID | Requirement |
|---|---|
| FR-9.1 | The system shall notify the user if the input cannot be parsed into a valid decision structure. |
| FR-9.2 | The system shall handle missing data gracefully without crashing. |

---

### FR-10: Decision Reset

| ID | Requirement |
|---|---|
| FR-10.1 | The system shall allow the user to reset and start a new decision after viewing results. |

---

## Non-Functional Requirements

Non-functional requirements define **how the system must behave** — quality attributes, constraints, and standards.

---

### NFR-1: Performance

| ID | Requirement |
|---|---|
| NFR-1.1 | The system shall return a complete decision result within **10 seconds** under normal load. |
| NFR-1.2 | LLM API calls shall have a maximum timeout of **8 seconds** before returning an error to the user. |

---

### NFR-2: Reliability

| ID | Requirement |
|---|---|
| NFR-2.1 | The system shall handle failed API calls with a clear user-facing error message. |
| NFR-2.2 | The system shall not crash or enter an undefined state due to unexpected user input. |

---

### NFR-3: Usability

| ID | Requirement |
|---|---|
| NFR-3.1 | A new user shall be able to complete a decision analysis without any onboarding or instructions. |
| NFR-3.2 | The interface shall display results in a layout that is scannable within 30 seconds. |
| NFR-3.3 | Error messages shall be written in plain language, not technical terms. |

---

### NFR-4: Maintainability

| ID | Requirement |
|---|---|
| NFR-4.1 | Backend modules (parser, scorer, retriever, explainer) shall be independently replaceable. |
| NFR-4.2 | All LLM prompts shall be stored in a single location for easy iteration. |
| NFR-4.3 | The codebase shall follow the code style guidelines defined in CONTRIBUTING.md. |

---

### NFR-5: Scalability

| ID | Requirement |
|---|---|
| NFR-5.1 | The scoring model shall support extension to more than 3 options without architectural changes. |
| NFR-5.2 | The data retrieval module shall be replaceable with a live API without breaking the interface contract. |

---

### NFR-6: Security

| ID | Requirement |
|---|---|
| NFR-6.1 | API keys shall never be committed to the repository. |
| NFR-6.2 | The system shall not store user decision inputs beyond the scope of a single request (MVP). |

---

### NFR-7: Portability

| ID | Requirement |
|---|---|
| NFR-7.1 | The backend shall run on any system with Python 3.10+ installed. |
| NFR-7.2 | The project shall include environment setup instructions sufficient for a new developer to run it locally. |
