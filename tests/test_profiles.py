import tempfile
import unittest
from pathlib import Path

from core.profiles import (
    FrameworkProfile,
    ProfileRegistry,
    detect_profile,
    detect_flutter_conventions,
    get_flutter_profile,
    get_android_profile,
    get_node_profile,
    get_generic_profile,
)

class TestFrameworkProfiles(unittest.TestCase):
    def test_detect_flutter_profile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "pubspec.yaml").write_text(
                "name: sample_app\ndependencies:\n  flutter:\n    sdk: flutter\n  flutter_bloc: ^8.0.0\n  get_it: ^7.0.0\n",
                encoding="utf-8",
            )
            (root / "lib" / "features").mkdir(parents=True)
            (root / "test").mkdir(parents=True)

            profile = detect_profile(root)
            self.assertEqual(profile.name, "flutter")
            self.assertEqual(profile.language, "Dart")
            self.assertEqual(profile.conventions.get("state_management"), "Bloc / Cubit")
            self.assertEqual(profile.conventions.get("dependency_injection"), "GetIt (Service Locator)")
            self.assertEqual(profile.conventions.get("architecture"), "Feature-First Clean Architecture")

            # Command resolution: test applies, integration_test is N/A because integration_test/ is missing
            resolved = profile.resolve_commands(root)
            self.assertTrue(resolved["test"].is_applicable)
            self.assertFalse(resolved["integration_test"].is_applicable)
            self.assertIn("N/A", resolved["integration_test"].skip_reason)

    def test_detect_node_profile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "package.json").write_text('{"name": "my-node-app", "scripts": {"test": "jest"}}', encoding="utf-8")
            profile = detect_profile(root)
            self.assertEqual(profile.name, "node")
            self.assertEqual(profile.framework, "Node.js")

    def test_detect_android_profile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "build.gradle").write_text("plugins { id 'com.android.application' }", encoding="utf-8")
            profile = detect_profile(root)
            self.assertEqual(profile.name, "android")

    def test_fallback_generic_profile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            profile = detect_profile(root)
            self.assertEqual(profile.name, "generic")

if __name__ == "__main__":
    unittest.main()
