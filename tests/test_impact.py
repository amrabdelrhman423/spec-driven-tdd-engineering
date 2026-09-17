import tempfile
import unittest
from pathlib import Path

from core.impact import ChangeScope, ImpactAnalyzer

class TestImpactAnalyzer(unittest.TestCase):
    def test_scope_all_expected_files(self):
        scope = ChangeScope(
            feature_name="cart",
            presentation=["lib/screens/cart_screen.dart"],
            state=["lib/cubits/cart_cubit.dart"],
            tests=["test/cart_cubit_test.dart"],
        )
        expected = scope.all_expected_files
        self.assertIn("cart_screen.dart", expected)
        self.assertIn("cart_cubit.dart", expected)
        self.assertIn("cart_cubit_test.dart", expected)

    def test_compare_detects_unexpected_files(self):
        scope = ChangeScope(
            feature_name="cart",
            presentation=["lib/cart_screen.dart"],
            tests=["test/cart_test.dart"],
        )
        actual = [
            "lib/cart_screen.dart",
            "test/cart_test.dart",
            "lib/unrelated_payment_engine.dart",  # UNEXPECTED
        ]
        analyzer = ImpactAnalyzer(Path("."))
        cmp = analyzer.compare(scope, actual_files=actual)
        self.assertTrue(cmp.has_unexpected_changes)
        self.assertIn("lib/unrelated_payment_engine.dart", cmp.unexpected_files)
        self.assertIn("WARNING: Unexpected Change", cmp.warning_message)

    def test_compare_clean_when_within_scope(self):
        scope = ChangeScope(
            feature_name="cart",
            presentation=["lib/cart_screen.dart"],
            tests=["test/cart_test.dart"],
        )
        actual = ["lib/cart_screen.dart", "test/cart_test.dart"]
        analyzer = ImpactAnalyzer(Path("."))
        cmp = analyzer.compare(scope, actual_files=actual)
        self.assertFalse(cmp.has_unexpected_changes)
        self.assertEqual(len(cmp.unexpected_files), 0)

    def test_save_and_load_scope(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            feat_dir = Path(tmpdir)
            analyzer = ImpactAnalyzer(feat_dir)
            scope = ChangeScope(
                feature_name="auth",
                presentation=["lib/login_screen.dart"],
                state=["lib/login_cubit.dart"],
                tests=["test/login_test.dart"],
            )
            saved = analyzer.save_expected_scope(feat_dir, scope)
            self.assertTrue(saved.exists())
            
            loaded = analyzer.load_expected_scope(feat_dir)
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.presentation, ["lib/login_screen.dart"])
            self.assertEqual(loaded.state, ["lib/login_cubit.dart"])
            self.assertEqual(loaded.tests, ["test/login_test.dart"])

if __name__ == "__main__":
    unittest.main()
