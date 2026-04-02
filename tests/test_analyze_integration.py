import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.decision import Criterion, Option, ParsedDecision
from backend.main import app


class TestAnalyzeDecisionIntegration(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("backend.main.generate_explanation")
    @patch("backend.main.parse_decision")
    def test_analyze_populates_parser_scorer_and_explanation(
        self, mock_parse_decision, mock_generate_explanation
    ):
        # Parser output fixture: this is what parse_decision should return.
        mock_parse_decision.return_value = ParsedDecision(
            question="Should I move to London or Berlin?",
            criteria=[
                Criterion(name="salary", weight=0.5),
                Criterion(name="career_opportunities", weight=0.5),
            ],
            options=[Option(name="London"), Option(name="Berlin")],
        )
        mock_generate_explanation.return_value = (
            "London ranks higher on salary and career opportunities."
        )

        response = self.client.post(
            "/api/decisions/analyze",
            json={"question": "Should I move to London or Berlin?"},
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()

        # Parser stage is connected and used.
        mock_parse_decision.assert_called_once_with(
            "Should I move to London or Berlin?"
        )

        # Scorer stage is connected: scores and recommendation are populated.
        self.assertIsInstance(body.get("options"), list)
        self.assertGreaterEqual(len(body["options"]), 2)
        for option in body["options"]:
            self.assertIsNotNone(option.get("score"))

        self.assertIsNotNone(body.get("recommended_option"))

        # Explanation stage is connected and populated from LLM generator call.
        mock_generate_explanation.assert_called_once()
        self.assertTrue(isinstance(body.get("explanation"), str))
        self.assertTrue(len(body["explanation"].strip()) > 0)


if __name__ == "__main__":
    unittest.main()
