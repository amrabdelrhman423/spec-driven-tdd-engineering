import tempfile
import unittest
from pathlib import Path

from core.orchestrator import WorkflowEngine, OrchestrationStatus, WorkflowStep
from core.risk import RiskLevel

class TestOrchestrator(unittest.TestCase):
    def test_orchestrator_halts_on_unapproved_spec_for_medium_risk(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            feat_dir = root / ".specify" / "specs" / "my-feature"
            feat_dir.mkdir(parents=True)
            (feat_dir / "spec.md").write_text("# Spec", encoding="utf-8")
            (feat_dir / "plan.md").write_text("# Plan", encoding="utf-8")
            (feat_dir / "tasks.md").write_text("# Tasks", encoding="utf-8")

            engine = WorkflowEngine(root)
            result = engine.run_feature("my-feature", override_risk=RiskLevel.MEDIUM)

            self.assertEqual(result.status, OrchestrationStatus.BLOCKED_PENDING_APPROVAL)
            self.assertEqual(result.current_step, WorkflowStep.SPECIFY)
            self.assertIn("Gate 2", result.required_gate)

    def test_orchestrator_resumes_when_gates_approved(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            feat_dir = root / ".specify" / "specs" / "low-risk-feat"
            feat_dir.mkdir(parents=True)
            (feat_dir / "spec.md").write_text("# Spec", encoding="utf-8")
            (feat_dir / "plan.md").write_text("# Plan", encoding="utf-8")
            (feat_dir / "tasks.md").write_text("# Tasks", encoding="utf-8")

            engine = WorkflowEngine(root)
            # Authorize all gates
            result = engine.run_feature("low-risk-feat", approved_gates=["all"], override_risk=RiskLevel.LOW)

            self.assertEqual(result.status, OrchestrationStatus.COMPLETED)
            self.assertEqual(result.current_step, WorkflowStep.EVIDENCE)
            self.assertTrue((feat_dir / "verification.md").exists())

if __name__ == "__main__":
    unittest.main()
