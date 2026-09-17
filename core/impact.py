"""
Change Impact Analysis Engine.
Estimates pre-implementation blast radius and verifies post-implementation actual file diffs.
Detects unintended modifications and flags unexpected blast radius creep.
"""

from dataclasses import dataclass, field
from pathlib import Path
import re
import subprocess
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class ChangeScope:
    feature_name: str
    presentation: List[str] = field(default_factory=list)
    state: List[str] = field(default_factory=list)
    domain: List[str] = field(default_factory=list)
    data: List[str] = field(default_factory=list)
    dependency_injection: List[str] = field(default_factory=list)
    tests: List[str] = field(default_factory=list)
    config: List[str] = field(default_factory=list)
    other: List[str] = field(default_factory=list)

    @property
    def all_expected_files(self) -> Set[str]:
        combined = set()
        for group in [
            self.presentation,
            self.state,
            self.domain,
            self.data,
            self.dependency_injection,
            self.tests,
            self.config,
            self.other,
        ]:
            for item in group:
                combined.add(Path(item).name.lower())
                combined.add(item.replace("\\", "/").lower())
        return combined

    def to_markdown(self) -> str:
        lines = [
            f"# Change Impact Analysis: {self.feature_name}",
            "",
            "## Expected Architectural Scope",
            "",
            "### Presentation Layer",
        ]
        lines.extend([f"- `{f}`" for f in self.presentation] or ["- *None*"])
        lines.extend(["", "### State Management"])
        lines.extend([f"- `{f}`" for f in self.state] or ["- *None*"])
        lines.extend(["", "### Domain Layer (Entities, UseCases, Repositories)"])
        lines.extend([f"- `{f}`" for f in self.domain] or ["- *None*"])
        lines.extend(["", "### Data Layer (DataSources, Models, DTOs)"])
        lines.extend([f"- `{f}`" for f in self.data] or ["- *None*"])
        lines.extend(["", "### Dependency Injection & Service Locator"])
        lines.extend([f"- `{f}`" for f in self.dependency_injection] or ["- *None*"])
        lines.extend(["", "### Automated Tests"])
        lines.extend([f"- `{f}`" for f in self.tests] or ["- *None*"])
        lines.extend(["", "### Configuration & Dependencies"])
        lines.extend([f"- `{f}`" for f in self.config] or ["- *None*"])
        if self.other:
            lines.extend(["", "### Other Modified Files"])
            lines.extend([f"- `{f}`" for f in self.other])
        lines.append("")
        return "\n".join(lines)


@dataclass
class ImpactComparison:
    expected_files: Set[str]
    actual_files: Set[str]
    matched_files: Set[str]
    unmodified_expected: Set[str]
    unexpected_files: Set[str]
    has_unexpected_changes: bool
    warning_message: Optional[str] = None


class ImpactAnalyzer:
    """Computes expected changes and audits actual git changes against expectation."""

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir

    def save_expected_scope(self, feature_dir: Path, scope: ChangeScope) -> Path:
        """Save impact.md inside the feature spec directory."""
        path = feature_dir / "impact.md"
        path.write_text(scope.to_markdown(), encoding="utf-8")
        return path

    def load_expected_scope(self, feature_dir: Path) -> Optional[ChangeScope]:
        """Parse an existing impact.md into a ChangeScope."""
        path = feature_dir / "impact.md"
        if not path.exists():
            return None
        content = path.read_text(encoding="utf-8")
        feature_name = feature_dir.name

        def extract_items(section_title: str) -> List[str]:
            pattern = rf"### {re.escape(section_title)}\s*\n([\s\S]*?)(?=\n###|\n##|$)"
            match = re.search(pattern, content)
            if not match:
                return []
            items = []
            for line in match.group(1).splitlines():
                line = line.strip()
                m = re.match(r"^-\s*`([^`]+)`", line)
                if m and m.group(1) != "*None*":
                    items.append(m.group(1))
            return items

        return ChangeScope(
            feature_name=feature_name,
            presentation=extract_items("Presentation Layer"),
            state=extract_items("State Management"),
            domain=extract_items("Domain Layer (Entities, UseCases, Repositories)"),
            data=extract_items("Data Layer (DataSources, Models, DTOs)"),
            dependency_injection=extract_items("Dependency Injection & Service Locator"),
            tests=extract_items("Automated Tests"),
            config=extract_items("Configuration & Dependencies"),
            other=extract_items("Other Modified Files"),
        )

    def get_actual_changed_files(self) -> List[str]:
        """Detect actual modified or untracked files via git status."""
        try:
            res = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.root_dir,
                capture_output=True,
                text=True,
                check=True,
            )
            files = []
            for line in res.stdout.splitlines():
                line = line.strip()
                if len(line) > 3:
                    # git status format: XY filename
                    file_path = line[3:].strip()
                    # normalize path
                    files.append(file_path.replace("\\", "/"))
            return files
        except Exception:
            return []

    def compare(self, scope: ChangeScope, actual_files: Optional[List[str]] = None) -> ImpactComparison:
        """Compare expected files with actual files changed."""
        if actual_files is None:
            actual_files = self.get_actual_changed_files()

        actual_set = set(f.replace("\\", "/").lower() for f in actual_files)
        actual_names = set(Path(f).name.lower() for f in actual_files)

        expected_set = scope.all_expected_files

        matched = set()
        unexpected = set()

        for f in actual_files:
            f_norm = f.replace("\\", "/").lower()
            f_name = Path(f).name.lower()
            if f_norm in expected_set or f_name in expected_set:
                matched.add(f)
            else:
                unexpected.add(f)

        unmodified = set()
        for exp in expected_set:
            if exp not in actual_set and exp not in actual_names:
                unmodified.add(exp)

        has_unexpected = len(unexpected) > 0
        warning = None
        if has_unexpected:
            warning = (
                f"WARNING: Unexpected Change! The following {len(unexpected)} file(s) were modified "
                f"outside the expected change scope:\n" + "\n".join(f"  * {f}" for f in sorted(unexpected))
            )

        return ImpactComparison(
            expected_files=expected_set,
            actual_files=set(actual_files),
            matched_files=matched,
            unmodified_expected=unmodified,
            unexpected_files=unexpected,
            has_unexpected_changes=has_unexpected,
            warning_message=warning,
        )
