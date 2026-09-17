import tempfile
import unittest
from pathlib import Path

from core.doctor import run_doctor, ReadinessStatus

class TestDoctor(unittest.TestCase):
    def test_doctor_blocked_when_no_git_or_constitution(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = run_doctor(root)
            self.assertEqual(report.status, ReadinessStatus.BLOCKED)
            self.assertTrue(any(c.name == "Git repository" and c.status == "FAIL" for c in report.checks))
            self.assertTrue(any(c.name == "Constitution" and c.status == "FAIL" for c in report.checks))

    def test_doctor_warning_when_minimal_setup(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / ".git").mkdir()
            (root / ".specify").mkdir()
            (root / ".specify" / "constitution.md").write_text("# Constitution", encoding="utf-8")
            (root / "AGENTS.md").write_text("# Agents", encoding="utf-8")

            report = run_doctor(root)
            self.assertIn(report.status, [ReadinessStatus.WARNING, ReadinessStatus.READY])
            self.assertTrue(any(c.name == "Git repository" and c.status == "PASS" for c in report.checks))
            self.assertTrue(any(c.name == "Constitution" and c.status == "PASS" for c in report.checks))

if __name__ == "__main__":
    unittest.main()
