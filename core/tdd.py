"""
TDD Intent Validation & Execution Engine.
Distinguishes EXPECTED FAILURE (assertion red) from INFRASTRUCTURE FAILURE (compilation/import crash).
Captures explicit test-intent statements linking tests directly to spec requirements.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import re
from typing import Optional


class TestFailureType(str, Enum):
    EXPECTED_ASSERTION = "EXPECTED_ASSERTION"
    INFRASTRUCTURE_FAILURE = "INFRASTRUCTURE_FAILURE"
    UNEXPECTED_PASS = "UNEXPECTED_PASS"


@dataclass
class TestIntent:
    requirement_id: str
    behavior_proven: str
    expected_red_reason: str
    test_file: str
    test_name: str

    def to_markdown(self) -> str:
        return (
            f"### Test Intent: `{self.test_name}`\n"
            f"- **Requirement**: {self.requirement_id}\n"
            f"- **Behavior Proven**: {self.behavior_proven}\n"
            f"- **Expected RED Reason**: {self.expected_red_reason}\n"
            f"- **Target File**: `{self.test_file}`\n"
        )


@dataclass
class RedVerificationResult:
    is_valid_red: bool
    failure_type: TestFailureType
    summary: str
    output: str


def classify_test_failure(output: str, exit_code: int) -> RedVerificationResult:
    """Analyze test output to distinguish expected assertion failures from infrastructure/import crashes."""
    if exit_code == 0:
        return RedVerificationResult(
            is_valid_red=False,
            failure_type=TestFailureType.UNEXPECTED_PASS,
            summary="Test passed unexpectedly! Cannot claim RED phase when assertions pass.",
            output=output,
        )

    out_lower = output.lower()

    # Syntax and import errors indicate infrastructure failure, NOT valid red
    infra_markers = [
        "syntaxerror",
        "importerror",
        "modulenotfounderror",
        "compilation error",
        "cannot find module",
        "error: could not resolve",
        "fatal error",
        "target does not exist",
        "unhandled exception: file not found",
        "command not found",
    ]
    for marker in infra_markers:
        if marker in out_lower and not ("assertion" in out_lower or "failed" in out_lower):
            return RedVerificationResult(
                is_valid_red=False,
                failure_type=TestFailureType.INFRASTRUCTURE_FAILURE,
                summary=f"Infrastructure failure detected ({marker}). Fix build/syntax setup before declaring valid RED.",
                output=output,
            )

    # Valid assertion failure markers across Python, Dart/Flutter, Node, and JUnit
    assertion_markers = [
        "assertionerror",
        "expected:",
        "actual:",
        "failed:",
        "failures = 1",
        "failed 1 test",
        "test failed",
        "expect(",
        "assert",
    ]
    if any(marker in out_lower for marker in assertion_markers):
        return RedVerificationResult(
            is_valid_red=True,
            failure_type=TestFailureType.EXPECTED_ASSERTION,
            summary="Valid RED phase: Test failed as expected on domain assertion.",
            output=output,
        )

    return RedVerificationResult(
        is_valid_red=False,
        failure_type=TestFailureType.INFRASTRUCTURE_FAILURE,
        summary="Test exited with non-zero code, but no clear assertion failure was identified.",
        output=output,
    )
