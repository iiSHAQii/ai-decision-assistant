# Decision Analysis API

## Analyze decision

Submit a decision question and receive extracted criteria, scored options, and an explanation.

**Endpoint:** `POST ${API_BASE_URL}/api/decisions/analyze`

**Request**

- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Body:**

```json
{
  "question": "Should I move to London or Berlin? Salary and career opportunities are important to me."
}
```

The `question` value should be the user’s decision text, typically trimmed of leading/trailing whitespace.

**Expected response**

- **Status:** `200 OK`
- **Body:**

```json
{
  "criteria": [
    { "name": "Salary", "weight": 40 },
    { "name": "Career Opportunities", "weight": 40 },
    { "name": "Cost of Living", "weight": 20 }
  ],
  "options": [
    { "name": "London", "score": 7.5 },
    { "name": "Berlin", "score": 6.2 }
  ],
  "explanation": "London is recommended due to higher average salaries and better career opportunities, despite the higher cost of living."
}
```

| Field         | Type     | Description                                              |
|--------------|----------|----------------------------------------------------------|
| `criteria`   | array    | Extracted evaluation criteria, each with `name` and `weight` (e.g. 1–100). |
| `options`    | array    | Decision options with `name` and numeric `score`.        |
| `explanation`| string   | Natural-language summary of the recommendation.         |
