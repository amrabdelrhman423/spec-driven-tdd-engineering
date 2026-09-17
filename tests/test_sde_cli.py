import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.sde import main

class TestSDECLI(unittest.TestCase):
    def test_sde_doctor_runs(self):
        with patch("sys.argv", ["sde", "doctor"]):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
                try:
                    main()
                except SystemExit:
                    pass
                output = mock_out.getvalue()
                self.assertIn("SDE Repository Doctor", output)
                self.assertIn("Git repository", output)

    def test_sde_profile_detect(self):
        with patch("sys.argv", ["sde", "profile", "detect"]):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
                main()
                output = mock_out.getvalue()
                self.assertIn("Detected Profile", output)

    def test_sde_feature_risk_and_impact(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_root = Path(tmpdir)
            with patch("tools.sde.ROOT_DIR", test_root):
                # 1. Assess risk
                with patch("sys.argv", ["sde", "feature", "risk", "demo-feat", "--level", "high", "--security"]):
                    main()
                    risk_file = test_root / ".specify" / "specs" / "demo-feat" / "risk.md"
                    self.assertTrue(risk_file.exists())
                    self.assertIn("`HIGH`", risk_file.read_text(encoding="utf-8"))

                # 2. Record change scope
                with patch("sys.argv", [
                    "sde", "feature", "impact", "demo-feat",
                    "--presentation", "lib/view.dart",
                    "--state", "lib/cubit.dart"
                ]):
                    main()
                    impact_file = test_root / ".specify" / "specs" / "demo-feat" / "impact.md"
                    self.assertTrue(impact_file.exists())
                    self.assertIn("lib/view.dart", impact_file.read_text(encoding="utf-8"))

    def test_sde_feature_create_and_implement(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_root = Path(tmpdir)
            with patch("tools.sde.ROOT_DIR", test_root), patch("tools.speckit.SPECIFY_DIR", test_root / ".specify"):
                with patch("sys.argv", ["sde", "feature", "create", "login-flow", "--level", "medium"]):
                    main()
                    feat_dir = test_root / ".specify" / "specs" / "login-flow"
                    self.assertTrue((feat_dir / "spec.md").exists())
                    self.assertTrue((feat_dir / "plan.md").exists())
                    self.assertTrue((feat_dir / "tasks.md").exists())
                    self.assertTrue((feat_dir / "risk.md").exists())

                with patch("sys.argv", ["sde", "feature", "implement", "login-flow"]):
                    with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
                        main()
                        out = mock_out.getvalue()
                        self.assertIn("Implementation Status: login-flow", out)
                        self.assertIn("Next Active Task", out)

if __name__ == "__main__":
    unittest.main()

