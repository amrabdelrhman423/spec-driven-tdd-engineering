"""
SDE Workflow Orchestrator.
Coordinates Discover -> Spec -> Plan -> Tasks -> TDD -> Verify -> Evidence.
Respects risk-based HITL gates and halts when human approval is required.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import subprocess
from typing import Dict, List, Optional, Tuple

from .risk import RiskLevel, RiskAssessment, assess_risk, RiskFactors, load_risk_assessment
from .evidence import VerificationStatus, VerificationReport, VerificationItem, EvidenceCollector
from .impact import ChangeScope, ImpactAnalyzer
from .profiles import FrameworkProfile, detect_profile


class WorkflowStep(str, Enum):
    DISCOVER = "DISCOVER"
    SPECIFY = "SPECIFY"
    PLAN = "PLAN"
    TASKS = "TASKS"
    TDD = "TDD"
    VERIFY = "VERIFY"
    EVIDENCE = "EVIDENCE"


class OrchestrationStatus(str, Enum):
    COMPLETED = "COMPLETED"
    BLOCKED_PENDING_APPROVAL = "BLOCKED_PENDING_APPROVAL"
    FAILED = "FAILED"


@dataclass
class ExecutionResult:
    feature_name: str
    status: OrchestrationStatus
    current_step: WorkflowStep
    risk_level: RiskLevel
    message: str
    required_gate: Optional[str] = None
    verification_report: Optional[VerificationReport] = None


class WorkflowEngine:
    """Executes or drives the SDE lifecycle with strict HITL adherence."""

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.specify_dir = root_dir / ".specify"
        self.profile = detect_profile(root_dir)

    def get_feature_dir(self, feature: str) -> Path:
        feat_name = feature.strip().lower().replace("_", "-")
        return self.specify_dir / "specs" / feat_name

    def run_feature(
        self,
        feature_name: str,
        approved_gates: Optional[List[str]] = None,
        override_risk: Optional[RiskLevel] = None,
    ) -> ExecutionResult:
        """Run the orchestration pipeline for a feature."""
        approved = set(approved_gates or [])
        feat_dir = self.get_feature_dir(feature_name)
        feat_dir.mkdir(parents=True, exist_ok=True)

        # 1. Risk Assessment check / load
        risk_file = feat_dir / "risk.md"
        if risk_file.exists():
            assessment = load_risk_assessment(risk_file)
        else:
            assessment = assess_risk(
                feature_name=feature_name,
                factors=RiskFactors(),
                explicit_level=override_risk or RiskLevel.MEDIUM,
            )
            risk_file.write_text(assessment.to_markdown(), encoding="utf-8")

        # Step 0: Critical pre-authorization check
        if assessment.level == RiskLevel.CRITICAL:
            critical_gate = "Gate 0: Explicit Pre-Execution Human Authorization (CRITICAL OVERRIDE)"
            if critical_gate not in approved and "all" not in approved:
                return ExecutionResult(
                    feature_name=feature_name,
                    status=OrchestrationStatus.BLOCKED_PENDING_APPROVAL,
                    current_step=WorkflowStep.DISCOVER,
                    risk_level=assessment.level,
                    message=(
                        f"CRITICAL RISK CHANGE DETECTED.\n"
                        f"Reason: {assessment.rationale}\n"
                        f"Explicit human authorization required before executing any work."
                    ),
                    required_gate=critical_gate,
                )

        # 2. Spec Check / Scaffolding
        spec_file = feat_dir / "spec.md"
        if not spec_file.exists():
            return ExecutionResult(
                feature_name=feature_name,
                status=OrchestrationStatus.FAILED,
                current_step=WorkflowStep.SPECIFY,
                risk_level=assessment.level,
                message=f"Specification missing at {spec_file}. Scaffold with 'sde feature specify {feature_name}'.",
            )

        # Gate 2 Check: Spec Approval (required for Medium, High, Critical)
        gate_2 = "Gate 2: Specification Approval (spec.md)"
        if gate_2 in assessment.required_approvals and gate_2 not in approved and "all" not in approved:
            return ExecutionResult(
                feature_name=feature_name,
                status=OrchestrationStatus.BLOCKED_PENDING_APPROVAL,
                current_step=WorkflowStep.SPECIFY,
                risk_level=assessment.level,
                message=f"Specification review required for {assessment.level.value} risk feature. Review spec.md and approve.",
                required_gate=gate_2,
            )

        # 3. Technical Plan Check
        plan_file = feat_dir / "plan.md"
        if not plan_file.exists():
            return ExecutionResult(
                feature_name=feature_name,
                status=OrchestrationStatus.FAILED,
                current_step=WorkflowStep.PLAN,
                risk_level=assessment.level,
                message=f"Technical plan missing at {plan_file}. Scaffold with 'sde feature plan {feature_name}'.",
            )

        # Gate 3 Check: Technical Plan Approval (required for High, Critical)
        gate_3 = "Gate 3: Technical Blueprint & Contract Approval (plan.md)"
        if gate_3 in assessment.required_approvals and gate_3 not in approved and "all" not in approved:
            return ExecutionResult(
                feature_name=feature_name,
                status=OrchestrationStatus.BLOCKED_PENDING_APPROVAL,
                current_step=WorkflowStep.PLAN,
                risk_level=assessment.level,
                message=f"Technical plan approval required for {assessment.level.value} risk feature. Review plan.md and approve.",
                required_gate=gate_3,
            )

        # 4. Tasks Check
        tasks_file = feat_dir / "tasks.md"
        if not tasks_file.exists():
            return ExecutionResult(
                feature_name=feature_name,
                status=OrchestrationStatus.FAILED,
                current_step=WorkflowStep.TASKS,
                risk_level=assessment.level,
                message=f"Tasks list missing at {tasks_file}. Scaffold with 'sde feature tasks {feature_name}'.",
            )

        # 5. Verification & Evidence Collection
        collector = EvidenceCollector(feat_dir)
        report = VerificationReport(
            feature_name=feature_name,
            specification_status=VerificationStatus.PASS,
        )

        resolved_cmds = self.profile.resolve_commands(self.root_dir)

        # Run Test Command
        test_res = resolved_cmds.get("test")
        if test_res and test_res.is_applicable and test_res.command:
            try:
                proc = subprocess.run(
                    test_res.command,
                    shell=True,
                    cwd=self.root_dir,
                    capture_output=True,
                    text=True,
                )
                collector.record_log("tests.txt", proc.stdout + "\n" + proc.stderr)
                status = VerificationStatus.PASS if proc.returncode == 0 else VerificationStatus.FAIL
                summary = "All tests executed and passed." if proc.returncode == 0 else "Tests failed with exit code non-zero."
                report.tests_item = VerificationItem(
                    name="Unit/Widget Tests",
                    status=status,
                    command=test_res.command,
                    output_summary=summary,
                    evidence_file="tests.txt",
                )
            except Exception as e:
                report.tests_item = VerificationItem(
                    name="Unit/Widget Tests",
                    status=VerificationStatus.FAIL,
                    command=test_res.command,
                    output_summary=f"Failed to run test command: {e}",
                )
        else:
            reason = test_res.skip_reason if test_res else "No test command available"
            report.tests_item = VerificationItem(
                name="Unit/Widget Tests",
                status=VerificationStatus.NA,
                output_summary=reason,
            )

        # Run Analysis Command
        ana_res = resolved_cmds.get("analyze")
        if ana_res and ana_res.is_applicable and ana_res.command:
            try:
                proc = subprocess.run(
                    ana_res.command,
                    shell=True,
                    cwd=self.root_dir,
                    capture_output=True,
                    text=True,
                )
                collector.record_log("analysis.txt", proc.stdout + "\n" + proc.stderr)
                status = VerificationStatus.PASS if proc.returncode == 0 else VerificationStatus.FAIL
                summary = "Static analysis clean." if proc.returncode == 0 else "Static analysis reported issues."
                report.analysis_item = VerificationItem(
                    name="Static Analysis",
                    status=status,
                    command=ana_res.command,
                    output_summary=summary,
                    evidence_file="analysis.txt",
                )
            except Exception as e:
                report.analysis_item = VerificationItem(
                    name="Static Analysis",
                    status=VerificationStatus.FAIL,
                    command=ana_res.command,
                    output_summary=f"Failed to run analysis command: {e}",
                )
        else:
            report.analysis_item = VerificationItem(
                name="Static Analysis",
                status=VerificationStatus.NA,
                output_summary="No analysis command defined",
            )

        # Integration tests
        integ_res = resolved_cmds.get("integration_test")
        if not integ_res or not integ_res.is_applicable:
            report.integration_item = VerificationItem(
                name="Integration Tests",
                status=VerificationStatus.NA,
                output_summary=integ_res.skip_reason if integ_res else "N/A",
            )

        collector.write_verification_report(report)

        # Gate 7: Final Verification & Merge Sign-off
        gate_7 = "Gate 7: Final Verification & Merge Sign-Off"
        if gate_7 in assessment.required_approvals and gate_7 not in approved and "all" not in approved:
            return ExecutionResult(
                feature_name=feature_name,
                status=OrchestrationStatus.BLOCKED_PENDING_APPROVAL,
                current_step=WorkflowStep.VERIFY,
                risk_level=assessment.level,
                message=f"Verification complete. Final sign-off required for feature '{feature_name}'.",
                required_gate=gate_7,
                verification_report=report,
            )

        return ExecutionResult(
            feature_name=feature_name,
            status=OrchestrationStatus.COMPLETED,
            current_step=WorkflowStep.EVIDENCE,
            risk_level=assessment.level,
            message=f"Orchestration completed successfully for '{feature_name}' with evidence recorded.",
            verification_report=report,
        )
