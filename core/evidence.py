"""
Evidence-Driven Verification System.
Tracks and reports strictly executed outcomes: PASS, FAIL, NOT_RUN, BLOCKED, N/A.
Guarantees that unexecuted checks are never claimed as PASS.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional
import json


class VerificationStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_RUN = "NOT_RUN"
    BLOCKED = "BLOCKED"
    NA = "N/A"


@dataclass
class VerificationItem:
    name: str
    status: VerificationStatus = VerificationStatus.NOT_RUN
    command: Optional[str] = None
    output_summary: Optional[str] = None
    evidence_file: Optional[str] = None
    details: Dict[str, str] = field(default_factory=dict)


@dataclass
class DeviceVerificationDetails:
    device: str = "N/A"
    os: str = "N/A"
    scenario: str = "N/A"
    expected: str = "N/A"
    actual: str = "N/A"
    status: VerificationStatus = VerificationStatus.NA


@dataclass
class VerificationReport:
    feature_name: str
    specification_status: VerificationStatus = VerificationStatus.NOT_RUN
    tests_item: VerificationItem = field(default_factory=lambda: VerificationItem(name="Unit/Widget Tests"))
    analysis_item: VerificationItem = field(default_factory=lambda: VerificationItem(name="Static Analysis"))
    build_item: VerificationItem = field(default_factory=lambda: VerificationItem(name="Build"))
    integration_item: VerificationItem = field(default_factory=lambda: VerificationItem(name="Integration Tests", status=VerificationStatus.NA))
    device_details: DeviceVerificationDetails = field(default_factory=DeviceVerificationDetails)
    ci_status: VerificationStatus = VerificationStatus.NOT_RUN
    deployment_status: VerificationStatus = VerificationStatus.NA
    evidence_files: List[str] = field(default_factory=list)
    remaining_risks: List[str] = field(default_factory=list)

    @property
    def is_fully_passing(self) -> bool:
        """Returns True only if all active and executed verification items are PASS."""
        critical_items = [
            self.specification_status,
            self.tests_item.status,
            self.analysis_item.status,
        ]
        for item in critical_items:
            if item != VerificationStatus.PASS:
                return False
        # If build was attempted, it must pass
        if self.build_item.status not in (VerificationStatus.PASS, VerificationStatus.NA):
            return False
        # If integration tests were run, they must pass
        if self.integration_item.status not in (VerificationStatus.PASS, VerificationStatus.NA):
            return False
        # If device verification was attempted, it must pass
        if self.device_details.status not in (VerificationStatus.PASS, VerificationStatus.NA):
            return False
        return True

    def to_markdown(self) -> str:
        md = [
            f"# Verification Report: {self.feature_name}",
            "",
            "## Summary Status",
            f"- **Specification Compliance**: `{self.specification_status.value}`",
            f"- **Overall Suite Pass**: `{'PASS' if self.is_fully_passing else 'INCOMPLETE / FAIL'}`",
            "",
            "## 1. Specification & Acceptance Criteria",
            f"**Status**: `{self.specification_status.value}`  ",
            "",
            "## 2. Automated Tests",
            f"**Status**: `{self.tests_item.status.value}`  ",
            f"**Command**: `{self.tests_item.command or 'None'}`  ",
            f"**Result**: {self.tests_item.output_summary or 'No execution recorded.'}  ",
        ]
        if self.tests_item.evidence_file:
            md.append(f"**Evidence Log**: [`{self.tests_item.evidence_file}`](./evidence/{self.tests_item.evidence_file})")
        
        md.extend([
            "",
            "## 3. Static Analysis & Lint",
            f"**Status**: `{self.analysis_item.status.value}`  ",
            f"**Command**: `{self.analysis_item.command or 'None'}`  ",
            f"**Result**: {self.analysis_item.output_summary or 'No execution recorded.'}  ",
        ])
        if self.analysis_item.evidence_file:
            md.append(f"**Evidence Log**: [`{self.analysis_item.evidence_file}`](./evidence/{self.analysis_item.evidence_file})")

        md.extend([
            "",
            "## 4. Build Verification",
            f"**Status**: `{self.build_item.status.value}`  ",
            f"**Command**: `{self.build_item.command or 'None'}`  ",
            f"**Result**: {self.build_item.output_summary or 'No execution recorded.'}  ",
        ])
        if self.build_item.evidence_file:
            md.append(f"**Evidence Log**: [`{self.build_item.evidence_file}`](./evidence/{self.build_item.evidence_file})")

        md.extend([
            "",
            "## 5. Integration Tests",
            f"**Status**: `{self.integration_item.status.value}`  ",
            f"**Command**: `{self.integration_item.command or 'None'}`  ",
            f"**Result**: {self.integration_item.output_summary or 'N/A or not executed.'}  ",
        ])
        if self.integration_item.evidence_file:
            md.append(f"**Evidence Log**: [`{self.integration_item.evidence_file}`](./evidence/{self.integration_item.evidence_file})")

        md.extend([
            "",
            "## 6. Real Device Verification",
            f"**Status**: `{self.device_details.status.value}`  ",
            f"- **Device**: {self.device_details.device}",
            f"- **OS**: {self.device_details.os}",
            f"- **Scenario**: {self.device_details.scenario}",
            f"- **Expected**: {self.device_details.expected}",
            f"- **Actual**: {self.device_details.actual}",
            "",
            "## 7. CI Pipeline Status",
            f"**Status**: `{self.ci_status.value}`  ",
            "",
            "## 8. Deployment Status",
            f"**Status**: `{self.deployment_status.value}`  ",
            "",
            "## 9. Captured Evidence Artifacts",
        ])
        if self.evidence_files:
            for ef in self.evidence_files:
                md.append(f"- [`{ef}`](./evidence/{ef})")
        else:
            md.append("- *No evidence logs captured yet.*")

        md.extend([
            "",
            "## 10. Remaining Risks",
        ])
        if self.remaining_risks:
            for risk in self.remaining_risks:
                md.append(f"- [ ] {risk}")
        else:
            md.append("- None identified.")
        md.append("")
        return "\n".join(md)


class EvidenceCollector:
    """Manages recording of raw command outputs and artifacts into .specify/specs/<feature>/evidence/"""
    
    def __init__(self, feature_dir: Path):
        self.feature_dir = feature_dir
        self.evidence_dir = feature_dir / "evidence"
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        self.recorded_files: List[str] = []

    def record_log(self, filename: str, content: str) -> Path:
        """Write raw execution log to evidence directory."""
        file_path = self.evidence_dir / filename
        file_path.write_text(content, encoding="utf-8")
        if filename not in self.recorded_files:
            self.recorded_files.append(filename)
        return file_path

    def write_verification_report(self, report: VerificationReport) -> Path:
        """Write verification.md in the feature directory."""
        report.evidence_files = list(set(report.evidence_files + self.recorded_files))
        verif_path = self.feature_dir / "verification.md"
        verif_path.write_text(report.to_markdown(), encoding="utf-8")
        return verif_path
