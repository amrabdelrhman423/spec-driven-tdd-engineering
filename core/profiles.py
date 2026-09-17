"""
Framework Profiles & Command Resolution Engine.
Separates framework-agnostic Core from technology-specific commands and conventions.
Supports automatic detection, repository precedent inspection, and conditional command resolution.
"""

from dataclasses import dataclass, field
from pathlib import Path
import re
import shutil
from typing import Any, Dict, List, Optional


@dataclass
class ResolvedCommand:
    name: str
    command: Optional[str]
    is_applicable: bool
    skip_reason: Optional[str] = None


@dataclass
class FrameworkProfile:
    name: str
    platform: str
    language: str
    framework: str
    commands: Dict[str, str] = field(default_factory=dict)
    test_types: List[str] = field(default_factory=list)
    conventions: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def resolve_commands(self, root_dir: Path) -> Dict[str, ResolvedCommand]:
        """Dynamically resolve which commands apply to this specific repository."""
        resolved = {}
        
        # Analyze
        analyze_cmd = self.commands.get("analyze")
        resolved["analyze"] = ResolvedCommand(
            name="analyze",
            command=analyze_cmd,
            is_applicable=bool(analyze_cmd),
        )

        # Format
        format_cmd = self.commands.get("format")
        resolved["format"] = ResolvedCommand(
            name="format",
            command=format_cmd,
            is_applicable=bool(format_cmd),
        )

        # Unit / Main Tests
        test_cmd = self.commands.get("test")
        test_dir_exists = (root_dir / "test").is_dir() or (root_dir / "tests").is_dir()
        resolved["test"] = ResolvedCommand(
            name="test",
            command=test_cmd if test_dir_exists else None,
            is_applicable=test_dir_exists,
            skip_reason="No test/ or tests/ directory discovered" if not test_dir_exists else None,
        )

        # Integration Tests
        integ_cmd = self.commands.get("integration_test")
        integ_dir_exists = (
            (root_dir / "integration_test").is_dir()
            or (root_dir / "tests" / "integration").is_dir()
            or (root_dir / "e2e").is_dir()
        )
        resolved["integration_test"] = ResolvedCommand(
            name="integration_test",
            command=integ_cmd if (integ_cmd and integ_dir_exists) else None,
            is_applicable=bool(integ_cmd and integ_dir_exists),
            skip_reason="No integration_test/ or e2e/ directory found (marked N/A)" if not integ_dir_exists else None,
        )

        # Build
        build_cmd = self.commands.get("build")
        resolved["build"] = ResolvedCommand(
            name="build",
            command=build_cmd,
            is_applicable=bool(build_cmd),
        )

        return resolved


def detect_flutter_conventions(root_dir: Path) -> Dict[str, str]:
    """Inspect pubspec.yaml and lib/ to detect established architecture and libraries."""
    conventions = {
        "state_management": "setState (default)",
        "dependency_injection": "manual / constructor injection",
        "architecture": "feature-first / standard Flutter",
    }
    
    pubspec = root_dir / "pubspec.yaml"
    if not pubspec.exists():
        return conventions

    content = pubspec.read_text(encoding="utf-8")

    # State management detection
    if "flutter_bloc:" in content or "bloc:" in content:
        conventions["state_management"] = "Bloc / Cubit"
    elif "flutter_riverpod:" in content or "riverpod:" in content:
        conventions["state_management"] = "Riverpod"
    elif "provider:" in content:
        conventions["state_management"] = "Provider"
    elif "get:" in content or "getx:" in content:
        conventions["state_management"] = "GetX"

    # DI detection
    if "get_it:" in content:
        conventions["dependency_injection"] = "GetIt (Service Locator)"
    elif "injectable:" in content:
        conventions["dependency_injection"] = "Injectable + GetIt"

    # Architecture detection
    lib_dir = root_dir / "lib"
    if lib_dir.is_dir():
        children = [c.name.lower() for c in lib_dir.iterdir() if c.is_dir()]
        if any(c in children for c in ["core", "features"]):
            conventions["architecture"] = "Feature-First Clean Architecture"
        elif any(c in children for c in ["domain", "data", "presentation"]):
            conventions["architecture"] = "Layer-First Clean Architecture"
        elif "blocs" in children or "cubits" in children or "screens" in children:
            conventions["architecture"] = "Layer-Oriented MVC/MVVM"

    return conventions


def get_flutter_profile(root_dir: Path) -> FrameworkProfile:
    """Build the official Flutter Profile configured for the target repository."""
    conventions = detect_flutter_conventions(root_dir)
    return FrameworkProfile(
        name="flutter",
        platform="mobile_desktop_web",
        language="Dart",
        framework="Flutter",
        commands={
            "analyze": "flutter analyze",
            "format": "dart format --output=none --set-exit-if-changed .",
            "test": "flutter test",
            "integration_test": "flutter test integration_test",
            "build_apk": "flutter build apk",
            "build_appbundle": "flutter build appbundle",
            "build_ipa": "flutter build ipa",
            "build": "flutter build apk",
        },
        test_types=["unit", "widget", "integration", "golden"],
        conventions=conventions,
        metadata={
            "has_flutter_cli": shutil.which("flutter") is not None,
            "has_dart_cli": shutil.which("dart") is not None,
        },
    )


def get_android_profile(root_dir: Path) -> FrameworkProfile:
    """Build Android Profile."""
    gradlew = "./gradlew" if (root_dir / "gradlew").exists() else "gradle"
    return FrameworkProfile(
        name="android",
        platform="mobile",
        language="Kotlin / Java",
        framework="Android SDK",
        commands={
            "analyze": f"{gradlew} lint",
            "format": f"{gradlew} ktlintCheck",
            "test": f"{gradlew} testDebugUnitTest",
            "integration_test": f"{gradlew} connectedAndroidTest",
            "build": f"{gradlew} assembleDebug",
        },
        test_types=["unit", "instrumentation"],
        conventions={"architecture": "Clean Architecture / MVVM", "dependency_injection": "Hilt / Dagger"},
    )


def get_node_profile(root_dir: Path) -> FrameworkProfile:
    """Build Node.js Profile."""
    package_json = root_dir / "package.json"
    test_cmd = "npm test"
    if package_json.exists():
        text = package_json.read_text(encoding="utf-8")
        if '"test"' not in text:
            test_cmd = "node --test"
    return FrameworkProfile(
        name="node",
        platform="backend_fullstack",
        language="JavaScript / TypeScript",
        framework="Node.js",
        commands={
            "analyze": "npm run lint",
            "format": "npm run format",
            "test": test_cmd,
            "integration_test": "npm run test:e2e",
            "build": "npm run build",
        },
        test_types=["unit", "integration", "e2e"],
        conventions={"architecture": "Modular / Layered", "dependency_injection": "Inversify / NestJS / Native"},
    )


def get_generic_profile(root_dir: Path) -> FrameworkProfile:
    """Fallback Generic Profile."""
    return FrameworkProfile(
        name="generic",
        platform="agnostic",
        language="Agnostic",
        framework="Generic",
        commands={
            "analyze": "python -m pyflakes .",
            "format": "python -m black --check .",
            "test": "python -m unittest",
            "integration_test": None,
            "build": None,
        },
        test_types=["unit", "integration"],
        conventions={"architecture": "Modular"},
    )


class ProfileRegistry:
    """Registry and factory for framework profiles."""

    def __init__(self, profiles_dir: Optional[Path] = None):
        self.profiles_dir = profiles_dir

    def detect(self, root_dir: Path) -> FrameworkProfile:
        """Auto-detect the appropriate profile based on repository markers."""
        # 1. Flutter check
        if (root_dir / "pubspec.yaml").exists():
            pub_content = (root_dir / "pubspec.yaml").read_text(encoding="utf-8", errors="ignore")
            if "flutter:" in pub_content or "flutter_test:" in pub_content:
                return get_flutter_profile(root_dir)

        # 2. Android check
        if (root_dir / "build.gradle").exists() or (root_dir / "app" / "build.gradle").exists():
            return get_android_profile(root_dir)

        # 3. Node check
        if (root_dir / "package.json").exists():
            return get_node_profile(root_dir)

        # 4. Fallback Generic
        return get_generic_profile(root_dir)


def detect_profile(root_dir: Path) -> FrameworkProfile:
    """Convenience helper to auto-detect framework profile."""
    return ProfileRegistry().detect(root_dir)
