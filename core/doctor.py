"""
SDE Doctor: Comprehensive Repository & Workflow Readiness Diagnostic Engine.
Inspects Git, Constitution, Agents, Skills, Profiles, Tests, CI, and reports READY/WARNING/BLOCKED.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import shutil
import subprocess
from typing import Dict, List, Optional, Tuple

from .profiles import detect_profile, FrameworkProfile


class ReadinessStatus(str, Enum):
    READY = "READY"
    WARNING = "WARNING"
    BLOCKED = "BLOCKED"


@dataclass
class DiagnosticCheck:
    name: str
    status: str  # "PASS", "WARN", "FAIL"
    message: str
    is_critical: bool = False


@dataclass
class DoctorReport:
    status: ReadinessStatus
    profile: FrameworkProfile
    checks: List[DiagnosticCheck] = field(default_factory=list)
    summary: str = ""

    def to_console(self) -> str:
        lines = ["\n=== SDE Repository Doctor ===", ""]
        icon_map = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]"}
        for c in self.checks:
            lines.append(f"{icon_map.get(c.status, '[INFO]'):<7} {c.name:<32} {c.message}")
        lines.append("")
        lines.append(f"Detected Profile    : {self.profile.name.upper()} ({self.profile.language})")
        lines.append(f"Architecture/Conv   : {self.profile.conventions.get('architecture', 'Standard')}")
        lines.append(f"State Management    : {self.profile.conventions.get('state_management', 'N/A')}")
        lines.append(f"Dependency Inject   : {self.profile.conventions.get('dependency_injection', 'N/A')}")
        lines.append("")
        lines.append(f"Repository Readiness: {self.status.value}")
        if self.summary:
            lines.append(f"Summary: {self.summary}")
        lines.append("")
        return "\n".join(lines)


def run_doctor(root_dir: Path) -> DoctorReport:
    """Run full diagnostic checks across the target workspace."""
    checks: List[DiagnosticCheck] = []
    
    # 1. Git Repository
    git_dir = root_dir / ".git"
    if git_dir.is_dir():
        checks.append(DiagnosticCheck("Git repository", "PASS", "Initialized"))
    else:
        checks.append(DiagnosticCheck("Git repository", "FAIL", "Missing .git directory", is_critical=True))

    # 2. Constitution
    constitution = root_dir / ".specify" / "constitution.md"
    if constitution.is_file():
        checks.append(DiagnosticCheck("Constitution", "PASS", "Found at .specify/constitution.md"))
    else:
        checks.append(DiagnosticCheck("Constitution", "FAIL", "Missing .specify/constitution.md (run sde init)", is_critical=True))

    # 3. Agent Instructions
    has_agents_md = (root_dir / "AGENTS.md").is_file()
    has_gemini_md = (root_dir / "GEMINI.md").is_file()
    has_claude_md = (root_dir / "CLAUDE.md").is_file()
    if has_agents_md and (has_gemini_md or has_claude_md):
        checks.append(DiagnosticCheck("Agent instructions", "PASS", "Configured (AGENTS, GEMINI, CLAUDE)"))
    elif has_agents_md:
        checks.append(DiagnosticCheck("Agent instructions", "PASS", "Configured (AGENTS.md)"))
    else:
        checks.append(DiagnosticCheck("Agent instructions", "WARN", "No AGENTS.md found in workspace root"))

    # 4. Skills Installation
    skills_dir = root_dir / ".agents" / "skills"
    has_sde_skill = (skills_dir / "spec-driven-tdd-engineering" / "SKILL.md").is_file()
    if has_sde_skill:
        checks.append(DiagnosticCheck("Skills", "PASS", "spec-driven-tdd-engineering active"))
    elif skills_dir.is_dir():
        checks.append(DiagnosticCheck("Skills", "WARN", "Skills directory exists but spec-driven-tdd-engineering not found"))
    else:
        checks.append(DiagnosticCheck("Skills", "WARN", "No .agents/skills/ directory detected"))

    # 5. SDD & TDD Configuration
    specs_dir = root_dir / ".specify" / "specs"
    if specs_dir.is_dir():
        checks.append(DiagnosticCheck("SDD configuration", "PASS", f"Active ({len(list(specs_dir.iterdir()))} specs found)"))
    else:
        checks.append(DiagnosticCheck("SDD configuration", "WARN", "No specs scaffolded in .specify/specs/"))

    # 6. Profile & Framework Detection
    profile = detect_profile(root_dir)
    checks.append(DiagnosticCheck(f"Framework profile ({profile.name})", "PASS", f"Language: {profile.language}"))

    # Check CLI tool presence for the framework
    if profile.name == "flutter":
        flutter_bin = shutil.which("flutter")
        if flutter_bin:
            checks.append(DiagnosticCheck("Flutter CLI", "PASS", f"Found at {flutter_bin}"))
        else:
            checks.append(DiagnosticCheck("Flutter CLI", "WARN", "flutter not found in PATH"))
    elif profile.name == "node":
        node_bin = shutil.which("node")
        if node_bin:
            checks.append(DiagnosticCheck("Node runtime", "PASS", f"Found at {node_bin}"))
        else:
            checks.append(DiagnosticCheck("Node runtime", "WARN", "node not found in PATH"))

    # 7. Test Commands Resolution
    resolved = profile.resolve_commands(root_dir)
    test_cmd = resolved.get("test")
    if test_cmd and test_cmd.is_applicable:
        checks.append(DiagnosticCheck("Test command", "PASS", f"`{test_cmd.command}`"))
    else:
        reason = test_cmd.skip_reason if test_cmd else "No test command defined"
        checks.append(DiagnosticCheck("Test command", "WARN", reason))

    # 8. Integration Tests Resolution
    integ_cmd = resolved.get("integration_test")
    if integ_cmd and integ_cmd.is_applicable:
        checks.append(DiagnosticCheck("Integration tests", "PASS", f"`{integ_cmd.command}`"))
    else:
        reason = integ_cmd.skip_reason if integ_cmd else "No integration test suite configured (N/A)"
        checks.append(DiagnosticCheck("Integration tests", "PASS", reason))

    # 9. CI / CD Configuration
    ci_dir = root_dir / ".github" / "workflows"
    has_ci = ci_dir.is_dir() and any(ci_dir.iterdir())
    if has_ci:
        checks.append(DiagnosticCheck("CI configuration", "PASS", "GitHub Actions workflows detected"))
    else:
        checks.append(DiagnosticCheck("CI configuration", "WARN", "No CI workflows in .github/workflows/"))

    # Overall Status Computation
    has_critical_fail = any(c.status == "FAIL" and c.is_critical for c in checks)
    has_any_fail = any(c.status == "FAIL" for c in checks)
    has_any_warn = any(c.status == "WARN" for c in checks)

    if has_critical_fail:
        status = ReadinessStatus.BLOCKED
        summary = "Critical setup elements missing. Address FAIL items before proceeding."
    elif has_any_fail or has_any_warn:
        status = ReadinessStatus.WARNING
        summary = "Workspace operational with warnings. Review highlighted recommendations."
    else:
        status = ReadinessStatus.READY
        summary = "All repository and engineering configurations verified."

    return DoctorReport(status=status, profile=profile, checks=checks, summary=summary)
