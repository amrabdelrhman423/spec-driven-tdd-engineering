import tempfile
import unittest
from pathlib import Path

from core.risk import (
    RiskLevel,
    RiskFactors,
    RiskAssessment,
    assess_risk,
    evaluate_hitl_gates,
    load_risk_assessment,
)

class TestRiskEngine(unittest.TestCase):
    def test_low_risk_classification(self):
        factors = RiskFactors()  # all False
        assessment = assess_risk("button-color", factors)
        self.assertEqual(assessment.level, RiskLevel.LOW)
        self.assertIn("Gate 7", assessment.required_approvals[0])
        # Fast track: only 1 gate (Gate 7)
        self.assertEqual(len(assessment.required_approvals), 1)

    def test_medium_risk_classification(self):
        factors = RiskFactors(production_impact=True)
        assessment = assess_risk("order-status", factors)
        self.assertEqual(assessment.level, RiskLevel.MEDIUM)
        self.assertTrue(any("Gate 2" in g for g in assessment.required_approvals))
        self.assertTrue(any("Gate 7" in g for g in assessment.required_approvals))

    def test_high_risk_classification(self):
        factors = RiskFactors(security_sensitive=True)
        assessment = assess_risk("jwt-auth", factors)
        self.assertEqual(assessment.level, RiskLevel.HIGH)
        self.assertTrue(any("Gate 2" in g for g in assessment.required_approvals))
        self.assertTrue(any("Gate 3" in g for g in assessment.required_approvals))
        self.assertTrue(any("Gate 7" in g for g in assessment.required_approvals))

    def test_critical_risk_classification(self):
        factors = RiskFactors(irreversible_deletion=True)
        assessment = assess_risk("purge-db", factors)
        self.assertEqual(assessment.level, RiskLevel.CRITICAL)
        self.assertTrue(any("Gate 0" in g for g in assessment.required_approvals))
        self.assertTrue(any("CRITICAL OVERRIDE" in g for g in assessment.required_approvals))

    def test_markdown_serialization_roundtrip(self):
        factors = RiskFactors(breaking_change=True, production_impact=True)
        assessment = assess_risk("api-v2", factors, rationale="Breaking public API endpoints.")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            risk_file = Path(tmpdir) / "risk.md"
            risk_file.write_text(assessment.to_markdown(), encoding="utf-8")
            
            loaded = load_risk_assessment(risk_file)
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.level, RiskLevel.HIGH)
            self.assertTrue(loaded.factors.breaking_change)
            self.assertTrue(loaded.factors.production_impact)
            self.assertIn("Breaking public API endpoints", loaded.rationale)

if __name__ == "__main__":
    unittest.main()
