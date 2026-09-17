"""
Risk Assessment & Risk-Based Human-in-the-Loop (HITL) Evaluation Engine.
Provides classification into LOW, MEDIUM, HIGH, and CRITICAL risk levels.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional
import json


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class RiskFactors:
    architecture_change: bool = False
    security_sensitive: bool = False
    data_migration: bool = False
    production_impact: bool = False
    breaking_change: bool = False
    irreversible_deletion: bool = False

    def to_dict(self) -> Dict[str, bool]:
        return {
            "architecture_change": self.architecture_change,
            "security_sensitive": self.security_sensitive,
            "data_migration": self.data_migration,
            "production_impact": self.production_impact,
            "breaking_change": self.breaking_change,
            "irreversible_deletion": self.irreversible_deletion,
        }


@dataclass
class RiskAssessment:
    feature_name: str
    level: RiskLevel
    factors: RiskFactors
    rationale: str
    required_approvals: List[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = [
            f"# Risk Assessment: {self.feature_name}",
            "",
            f"**Assessed Level**: `{self.level.value}`  ",
            f"**Workflow Mode**: `{'Fast Track' if self.level == RiskLevel.LOW else 'Standard Human Gate' if self.level == RiskLevel.MEDIUM else 'High Oversight' if self.level == RiskLevel.HIGH else 'Strict Critical Approval'}`",
            "",
            "## Risk Factors",
            f"- **Architecture Change**: `{'YES' if self.factors.architecture_change else 'NO'}`",
            f"- **Security Sensitive / PII**: `{'YES' if self.factors.security_sensitive else 'NO'}`",
            f"- **Data Migration**: `{'YES' if self.factors.data_migration else 'NO'}`",
            f"- **Production Impact**: `{'YES' if self.factors.production_impact else 'NO'}`",
            f"- **Breaking API / Contract Change**: `{'YES' if self.factors.breaking_change else 'NO'}`",
            f"- **Irreversible / Destructive Operation**: `{'YES' if self.factors.irreversible_deletion else 'NO'}`",
            "",
            "## Rationale",
            self.rationale.strip(),
            "",
            "## Mandatory Human Review Gates",
        ]
        if not self.required_approvals:
            lines.append("- [ ] **No intermediate mandatory pauses** (Fast-track workflow enabled for LOW risk).")
        else:
            for gate in self.required_approvals:
                lines.append(f"- [ ] **{gate}**")
        lines.append("")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "feature_name": self.feature_name,
            "level": self.level.value,
            "factors": self.factors.to_dict(),
            "rationale": self.rationale,
            "required_approvals": self.required_approvals,
        }


def assess_risk(
    feature_name: str,
    factors: RiskFactors,
    rationale: Optional[str] = None,
    explicit_level: Optional[RiskLevel] = None,
) -> RiskAssessment:
    """Assess risk level and required approval gates based on factors."""
    if explicit_level:
        level = explicit_level
    elif factors.irreversible_deletion or (factors.data_migration and factors.production_impact):
        level = RiskLevel.CRITICAL
    elif factors.security_sensitive or factors.breaking_change or factors.architecture_change:
        level = RiskLevel.HIGH
    elif factors.production_impact or factors.data_migration:
        level = RiskLevel.MEDIUM
    else:
        level = RiskLevel.LOW

    # Determine required gates based on risk level
    gates = evaluate_hitl_gates(level)

    # Generate rationale if not provided
    if not rationale:
        reasons = []
        if factors.irreversible_deletion:
            reasons.append("Irreversible data deletion or credential modification detected.")
        if factors.security_sensitive:
            reasons.append("Security-sensitive logic, authentication, or PII touched.")
        if factors.breaking_change:
            reasons.append("Breaking changes to public interfaces or contracts.")
        if factors.architecture_change:
            reasons.append("Major architectural modification or subsystem redesign.")
        if factors.data_migration:
            reasons.append("Database schema migration or data transformation involved.")
        if factors.production_impact:
            reasons.append("Direct impact on production runtime behavior.")
        if not reasons:
            reasons.append("Low-complexity or cosmetic changes with bounded local blast radius.")
        rationale = " ".join(reasons)

    return RiskAssessment(
        feature_name=feature_name,
        level=level,
        factors=factors,
        rationale=rationale,
        required_approvals=gates,
    )


def evaluate_hitl_gates(level: RiskLevel) -> List[str]:
    """Return the list of mandatory human review gates for a given risk level."""
    if level == RiskLevel.LOW:
        # Fast track: No blocking gates between spec/plan/TDD. Final check only.
        return ["Gate 7: Final Verification & Merge Sign-Off"]
    elif level == RiskLevel.MEDIUM:
        return [
            "Gate 2: Specification Approval (spec.md)",
            "Gate 7: Final Verification & Merge Sign-Off",
        ]
    elif level == RiskLevel.HIGH:
        return [
            "Gate 2: Specification Approval (spec.md)",
            "Gate 3: Technical Blueprint & Contract Approval (plan.md)",
            "Gate 7: Final Verification & Merge Sign-Off",
        ]
    elif level == RiskLevel.CRITICAL:
        return [
            "Gate 0: Explicit Pre-Execution Human Authorization (CRITICAL OVERRIDE)",
            "Gate 2: Specification Approval (spec.md)",
            "Gate 3: Technical Blueprint & Contract Approval (plan.md)",
            "Gate 4: Task Execution Authorization (tasks.md)",
            "Gate 7: Final Verification & Deployment Sign-Off",
        ]
    return ["Gate 7: Final Verification & Merge Sign-Off"]


def load_risk_assessment(path: Path) -> Optional[RiskAssessment]:
    """Parse a risk.md file back into RiskAssessment."""
    if not path.exists():
        return None
    content = path.read_text(encoding="utf-8")
    
    level = RiskLevel.LOW
    for lvl in [RiskLevel.CRITICAL, RiskLevel.HIGH, RiskLevel.MEDIUM, RiskLevel.LOW]:
        if f"`{lvl.value}`" in content:
            level = lvl
            break
            
    feature_name = path.parent.name
    factors = RiskFactors(
        architecture_change="Architecture Change**: `YES`" in content,
        security_sensitive="Security Sensitive / PII**: `YES`" in content,
        data_migration="Data Migration**: `YES`" in content,
        production_impact="Production Impact**: `YES`" in content,
        breaking_change="Breaking API / Contract Change**: `YES`" in content,
        irreversible_deletion="Irreversible / Destructive Operation**: `YES`" in content,
    )
    
    rationale = "Loaded from risk artifact."
    if "## Rationale" in content:
        parts = content.split("## Rationale")[1].split("## Mandatory Human Review Gates")[0]
        rationale = parts.strip()
        
    gates = evaluate_hitl_gates(level)
    return RiskAssessment(
        feature_name=feature_name,
        level=level,
        factors=factors,
        rationale=rationale,
        required_approvals=gates,
    )
