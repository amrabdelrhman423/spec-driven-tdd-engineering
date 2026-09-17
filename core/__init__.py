"""
SDE Core: Framework-Agnostic AI Software Engineering System.
Enforces SDD, TDD, Risk-Based HITL, Evidence-Driven Verification, and Change Impact Analysis.
"""

from .risk import RiskLevel, RiskAssessment, assess_risk, evaluate_hitl_gates
from .evidence import VerificationStatus, VerificationReport, EvidenceCollector
from .impact import ChangeScope, ImpactAnalyzer
from .profiles import FrameworkProfile, ProfileRegistry, detect_profile
from .doctor import DoctorReport, run_doctor
from .orchestrator import WorkflowEngine, WorkflowStep, ExecutionResult

__all__ = [
    "RiskLevel",
    "RiskAssessment",
    "assess_risk",
    "evaluate_hitl_gates",
    "VerificationStatus",
    "VerificationReport",
    "EvidenceCollector",
    "ChangeScope",
    "ImpactAnalyzer",
    "FrameworkProfile",
    "ProfileRegistry",
    "detect_profile",
    "DoctorReport",
    "run_doctor",
    "WorkflowEngine",
    "WorkflowStep",
    "ExecutionResult",
]
