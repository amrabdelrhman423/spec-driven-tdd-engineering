import io
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.speckit import (
    cmd_init,
    cmd_specify,
    cmd_plan,
    cmd_tasks,
    cmd_status,
    SPECIFY_DIR
)

class TestSpecKitCLI(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.patcher = patch("tools.speckit.SPECIFY_DIR", self.test_dir / ".specify")
        self.mock_specify_dir = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_init_creates_constitution(self):
        class Args:
            pass
        cmd_init(Args())
        const_path = self.mock_specify_dir / "constitution.md"
        self.assertTrue(const_path.exists())
        self.assertIn("Constitution", const_path.read_text(encoding="utf-8"))

    def test_specify_creates_feature_spec(self):
        class Args:
            feature = "payment-gateway"
            force = False
        cmd_specify(Args())
        spec_path = self.mock_specify_dir / "specs" / "payment-gateway" / "spec.md"
        self.assertTrue(spec_path.exists())
        self.assertIn("Payment Gateway", spec_path.read_text(encoding="utf-8"))

    def test_plan_creates_technical_plan(self):
        class Args:
            feature = "payment-gateway"
            force = False
        cmd_plan(Args())
        plan_path = self.mock_specify_dir / "specs" / "payment-gateway" / "plan.md"
        self.assertTrue(plan_path.exists())
        self.assertIn("Payment Gateway", plan_path.read_text(encoding="utf-8"))

    def test_tasks_creates_implementation_tasks(self):
        class Args:
            feature = "payment-gateway"
            force = False
        cmd_tasks(Args())
        tasks_path = self.mock_specify_dir / "specs" / "payment-gateway" / "tasks.md"
        self.assertTrue(tasks_path.exists())
        self.assertIn("Payment Gateway", tasks_path.read_text(encoding="utf-8"))

    def test_status_displays_feature_overview(self):
        class Args:
            feature = "search-service"
            force = False
        cmd_specify(Args())
        cmd_plan(Args())
        cmd_tasks(Args())

        with patch("sys.stdout", new_callable=io.StringIO) as mock_out:
            cmd_status(Args())
            output = mock_out.getvalue()
            self.assertIn("search-service", output)
            self.assertIn("YES", output)

if __name__ == "__main__":
    unittest.main()
