#!/usr/bin/env python3
"""
SDE CLI: AI Software Engineering System Orchestrator.
Unified tool for SDD, TDD, Risk-based HITL, Evidence verification, and Framework Profiles.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

# Add workspace root to sys.path so core can be imported directly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Console UTF-8 safety on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from core.risk import RiskLevel, RiskFactors, assess_risk, evaluate_hitl_gates, load_risk_assessment
from core.evidence import VerificationStatus, VerificationReport, EvidenceCollector, VerificationItem
from core.impact import ChangeScope, ImpactAnalyzer
from core.profiles import detect_profile, ProfileRegistry
from core.doctor import run_doctor
from core.orchestrator import WorkflowEngine, OrchestrationStatus
from tools.speckit import cmd_init, cmd_specify, cmd_plan, cmd_tasks, cmd_status, SPECIFY_DIR
from tools.skill_builder import validate_skill, sync_skills, scaffold_skill, parse_frontmatter


def cmd_sde_doctor(args):
    report = run_doctor(ROOT_DIR)
    print(report.to_console())
    if report.status == "BLOCKED":
        sys.exit(1)


def cmd_sde_run(args):
    feature = args.feature.strip().lower().replace("_", "-")
    approved = []
    if args.approve_all:
        approved.append("all")
    if args.approve:
        approved.extend(args.approve)

    engine = WorkflowEngine(ROOT_DIR)
    override_risk = None
    if args.risk:
        override_risk = RiskLevel(args.risk.upper())

    result = engine.run_feature(feature, approved_gates=approved, override_risk=override_risk)

    print(f"\n--- SDE Feature Run: {feature} ---")
    print(f"Risk Level : {result.risk_level.value}")
    print(f"Status     : {result.status.value}")
    print(f"Step       : {result.current_step.value}")
    print(f"\n{result.message}\n")

    if result.status == OrchestrationStatus.BLOCKED_PENDING_APPROVAL:
        print("=" * 65)
        print("ACTION REQUIRED: Human approval is mandatory before continuing.")
        print(f"Required Gate : {result.required_gate}")
        print(f"Resume with   : python tools/sde.py run {feature} --approve \"{result.required_gate}\"")
        print("=" * 65)
        sys.exit(2)
    elif result.status == OrchestrationStatus.FAILED:
        sys.exit(1)


def cmd_sde_feature_create(args):
    feature = args.feature.strip().lower().replace("_", "-")
    print(f"\n[INFO] Scaffolding complete feature: {feature}")
    cmd_specify(args)
    cmd_plan(args)
    cmd_tasks(args)
    cmd_sde_feature_risk(args)
    print(f"[SUCCESS] Feature '{feature}' fully scaffolded with spec, plan, tasks, and risk assessment.\n")


def cmd_sde_feature_risk(args):
    feature = args.feature.strip().lower().replace("_", "-")
    feat_dir = ROOT_DIR / ".specify" / "specs" / feature
    feat_dir.mkdir(parents=True, exist_ok=True)

    factors = RiskFactors(
        architecture_change=getattr(args, "architecture", False),
        security_sensitive=getattr(args, "security", False),
        data_migration=getattr(args, "migration", False),
        production_impact=getattr(args, "production", False),
        breaking_change=getattr(args, "breaking", False),
        irreversible_deletion=getattr(args, "destructive", False),
    )
    lvl_arg = getattr(args, "level", None)
    explicit_lvl = RiskLevel(lvl_arg.upper()) if lvl_arg else None
    rationale_arg = getattr(args, "rationale", None)
    assessment = assess_risk(feature, factors, rationale=rationale_arg, explicit_level=explicit_lvl)

    risk_path = feat_dir / "risk.md"
    risk_path.write_text(assessment.to_markdown(), encoding="utf-8")
    print(f"[SUCCESS] Assessed risk level '{assessment.level.value}' for feature '{feature}'")
    print(f"[SUCCESS] Saved artifact at: {risk_path}")


def cmd_sde_feature_impact(args):
    feature = args.feature.strip().lower().replace("_", "-")
    feat_dir = ROOT_DIR / ".specify" / "specs" / feature
    feat_dir.mkdir(parents=True, exist_ok=True)
    analyzer = ImpactAnalyzer(ROOT_DIR)

    if args.audit:
        scope = analyzer.load_expected_scope(feat_dir)
        if not scope:
            print(f"[WARN] No impact.md found at {feat_dir / 'impact.md'}. Run without --audit first.")
            return
        cmp = analyzer.compare(scope)
        print(f"\n=== Change Impact Audit: {feature} ===")
        print(f"Expected files: {len(cmp.expected_files)}")
        print(f"Actual modified files: {len(cmp.actual_files)}")
        print(f"Matched: {len(cmp.matched_files)}")
        if cmp.has_unexpected_changes:
            print(f"\n[FAIL] {cmp.warning_message}\n")
            sys.exit(1)
        else:
            print("[PASS] All modified files are within expected architectural scope.\n")
    else:
        # Create baseline impact.md
        scope = ChangeScope(
            feature_name=feature,
            presentation=args.presentation or [],
            state=args.state or [],
            domain=args.domain or [],
            data=args.data or [],
            dependency_injection=args.di or [],
            tests=args.tests or [],
            config=args.config or [],
        )
        saved = analyzer.save_expected_scope(feat_dir, scope)
        print(f"[SUCCESS] Saved change scope to: {saved}")


def cmd_sde_feature_test(args):
    feature = args.feature.strip().lower().replace("_", "-")
    profile = detect_profile(ROOT_DIR)
    resolved = profile.resolve_commands(ROOT_DIR)
    test_cmd = resolved.get("test")

    if not test_cmd or not test_cmd.is_applicable or not test_cmd.command:
        print(f"[WARN] No applicable test command for profile '{profile.name}' ({test_cmd.skip_reason if test_cmd else 'N/A'})")
        return

    print(f"\n[INFO] Running test command for {feature}: `{test_cmd.command}`")
    proc = subprocess.run(test_cmd.command, shell=True, cwd=ROOT_DIR)
    if proc.returncode == 0:
        print("[PASS] Tests completed successfully.")
    else:
        print(f"[FAIL] Tests exited with code {proc.returncode}.")
        sys.exit(proc.returncode)


def cmd_sde_feature_implement(args):
    feature = args.feature.strip().lower().replace("_", "-")
    tasks_file = ROOT_DIR / ".specify" / "specs" / feature / "tasks.md"
    if not tasks_file.exists():
        print(f"[ERROR] No tasks found at {tasks_file}. Run 'sde feature tasks {feature}' first.")
        sys.exit(1)

    text = tasks_file.read_text(encoding="utf-8")
    lines = text.splitlines()
    pending = [line.strip() for line in lines if line.strip().startswith("- [ ]")]
    completed = [line.strip() for line in lines if re.match(r"^-\s*\[[xX]\]", line.strip())]

    print(f"\n=== Implementation Status: {feature} ===")
    print(f"Completed: {len(completed)} task(s)")
    print(f"Remaining: {len(pending)} task(s)")
    if pending:
        print("\nNext Active Task:")
        print(f" -> {pending[0]}")
        print("\nGuidance: Follow TDD (Red -> Green -> Refactor). Witness assertion failure before writing code.")
    else:
        print("\nAll tasks marked complete! Proceed to 'sde feature verify'.")
    print()


def cmd_sde_feature_verify(args):
    feature = args.feature.strip().lower().replace("_", "-")
    feat_dir = ROOT_DIR / ".specify" / "specs" / feature
    if not feat_dir.exists():
        print(f"[ERROR] Feature directory does not exist: {feat_dir}")
        sys.exit(1)

    print(f"\n=== Running SDE Verification for: {feature} ===")
    engine = WorkflowEngine(ROOT_DIR)
    collector = EvidenceCollector(feat_dir)
    profile = engine.profile
    resolved_cmds = profile.resolve_commands(ROOT_DIR)

    report = VerificationReport(
        feature_name=feature,
        specification_status=VerificationStatus.PASS,
    )

    # 1. Tests
    test_res = resolved_cmds.get("test")
    if test_res and test_res.is_applicable and test_res.command:
        proc = subprocess.run(test_res.command, shell=True, cwd=ROOT_DIR, capture_output=True, text=True)
        collector.record_log("tests.txt", proc.stdout + "\n" + proc.stderr)
        status = VerificationStatus.PASS if proc.returncode == 0 else VerificationStatus.FAIL
        report.tests_item = VerificationItem(
            name="Tests",
            status=status,
            command=test_res.command,
            output_summary="Passed cleanly." if proc.returncode == 0 else "Execution failed.",
            evidence_file="tests.txt",
        )
    else:
        report.tests_item = VerificationItem(
            name="Tests",
            status=VerificationStatus.NA,
            output_summary=test_res.skip_reason if test_res else "N/A",
        )

    # 2. Static Analysis
    ana_res = resolved_cmds.get("analyze")
    if ana_res and ana_res.is_applicable and ana_res.command:
        proc = subprocess.run(ana_res.command, shell=True, cwd=ROOT_DIR, capture_output=True, text=True)
        collector.record_log("analysis.txt", proc.stdout + "\n" + proc.stderr)
        status = VerificationStatus.PASS if proc.returncode == 0 else VerificationStatus.FAIL
        report.analysis_item = VerificationItem(
            name="Static Analysis",
            status=status,
            command=ana_res.command,
            output_summary="Clean." if proc.returncode == 0 else "Issues found.",
            evidence_file="analysis.txt",
        )
    else:
        report.analysis_item = VerificationItem(name="Static Analysis", status=VerificationStatus.NA)

    verif_path = collector.write_verification_report(report)
    print(f"[SUCCESS] Verification report generated at: {verif_path}")
    print(f"Overall Status: {'PASS' if report.is_fully_passing else 'FAIL / INCOMPLETE'}\n")


def cmd_sde_profile(args):
    if args.profile_action == "detect":
        profile = detect_profile(ROOT_DIR)
        print(f"\nDetected Profile: {profile.name.upper()}")
        print(f"Platform        : {profile.platform}")
        print(f"Language        : {profile.language}")
        print(f"Framework       : {profile.framework}")
        print("\nResolved Commands:")
        for name, cmd in profile.resolve_commands(ROOT_DIR).items():
            status = f"`{cmd.command}`" if cmd.is_applicable else f"[N/A - {cmd.skip_reason}]"
            print(f" - {name:<18}: {status}")
        print("\nConventions:")
        for k, v in profile.conventions.items():
            print(f" - {k:<18}: {v}")
        print()
    elif args.profile_action == "list":
        profiles_dir = ROOT_DIR / "profiles"
        print("\nAvailable Framework Profiles:")
        if profiles_dir.is_dir():
            for p in profiles_dir.iterdir():
                if p.is_dir():
                    print(f" - {p.name}")
        print()


def cmd_sde_skill(args):
    if args.skill_action == "sync":
        synced = sync_skills(ROOT_DIR)
        print(f"[SUCCESS] Synced {len(synced)} skills to .claude/skills: {', '.join(synced)}")
    elif args.skill_action == "validate":
        agent_skills = ROOT_DIR / ".agents" / "skills"
        if not agent_skills.exists():
            print("No skills found to validate.")
            return
        all_passed = True
        for s in agent_skills.iterdir():
            if s.is_dir():
                issues = validate_skill(s)
                errors = [i for i in issues if not i.startswith("Warning:")]
                print(f"\n--- Checking: {s.name} ---")
                if errors:
                    all_passed = False
                    print(f"[FAIL] {len(errors)} error(s):")
                    for err in errors:
                        print(f"  * {err}")
                else:
                    print("[PASS] Frontmatter, structure, and links are valid.")
        if not all_passed:
            sys.exit(1)
    elif args.skill_action == "list":
        agent_skills = ROOT_DIR / ".agents" / "skills"
        print("Installed Skills:")
        if agent_skills.exists():
            for s in agent_skills.iterdir():
                if s.is_dir() and (s / "SKILL.md").exists():
                    try:
                        fm, _ = parse_frontmatter((s / "SKILL.md").read_text(encoding="utf-8"))
                        desc = fm.get("description", "")
                        print(f" - {s.name}: {desc[:80]}...")
                    except Exception:
                        print(f" - {s.name}")
    elif args.skill_action == "new":
        created = scaffold_skill(ROOT_DIR, args.name, getattr(args, "desc", None))
        print(f"[SUCCESS] Scaffolded new skill at: {created}")


def main():
    parser = argparse.ArgumentParser(
        prog="sde",
        description="SDE: AI Software Engineering System with SDD, TDD, Risk-based HITL & Verification",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # sde init
    subparsers.add_parser("init", help="Initialize .specify/ and repository constitution.md")

    # sde doctor
    subparsers.add_parser("doctor", help="Inspect workspace and report readiness (READY, WARNING, BLOCKED)")

    # sde status
    subparsers.add_parser("status", help="Show completion status across all specifications and tasks")

    # sde run <feature>
    run_parser = subparsers.add_parser("run", help="Orchestrate full SDD+TDD lifecycle for a feature")
    run_parser.add_argument("feature", help="Feature name (e.g. user-auth)")
    run_parser.add_argument("--risk", choices=["low", "medium", "high", "critical"], help="Override risk level")
    run_parser.add_argument("--approve", action="append", help="Approve a specific gate (repeatable)")
    run_parser.add_argument("--approve-all", action="store_true", help="Authorize all gates (Fast-track override)")

    # sde feature
    feat_parser = subparsers.add_parser("feature", help="Manage individual feature artifacts")
    feat_subs = feat_parser.add_subparsers(dest="feature_action", required=True)

    # sde feature create
    f_create = feat_subs.add_parser("create", help="Scaffold full feature (spec, plan, tasks, risk)")
    f_create.add_argument("feature", help="Feature name")
    f_create.add_argument("--level", choices=["low", "medium", "high", "critical"], default="medium")
    f_create.add_argument("--force", action="store_true")

    # sde feature specify
    f_spec = feat_subs.add_parser("specify", help="Scaffold feature specification (spec.md)")
    f_spec.add_argument("feature", help="Feature name")
    f_spec.add_argument("--force", action="store_true")

    # sde feature plan
    f_plan = feat_subs.add_parser("plan", help="Scaffold technical blueprint (plan.md)")
    f_plan.add_argument("feature", help="Feature name")
    f_plan.add_argument("--force", action="store_true")

    # sde feature tasks
    f_tasks = feat_subs.add_parser("tasks", help="Scaffold TDD implementation tasks (tasks.md)")
    f_tasks.add_argument("feature", help="Feature name")
    f_tasks.add_argument("--force", action="store_true")

    # sde feature risk
    f_risk = feat_subs.add_parser("risk", help="Assess risk and determine required HITL review gates")
    f_risk.add_argument("feature", help="Feature name")
    f_risk.add_argument("--level", choices=["low", "medium", "high", "critical"])
    f_risk.add_argument("--architecture", action="store_true", help="Major architecture modification")
    f_risk.add_argument("--security", action="store_true", help="Security-sensitive / PII")
    f_risk.add_argument("--migration", action="store_true", help="Data migration")
    f_risk.add_argument("--production", action="store_true", help="Production runtime impact")
    f_risk.add_argument("--breaking", action="store_true", help="Breaking API change")
    f_risk.add_argument("--destructive", action="store_true", help="Irreversible deletion")
    f_risk.add_argument("--rationale", help="Explanation for the risk classification")

    # sde feature impact
    f_impact = feat_subs.add_parser("impact", help="Manage and audit expected vs actual change scope")
    f_impact.add_argument("feature", help="Feature name")
    f_impact.add_argument("--presentation", nargs="*", help="Expected presentation files")
    f_impact.add_argument("--state", nargs="*", help="Expected state management files")
    f_impact.add_argument("--domain", nargs="*", help="Expected domain layer files")
    f_impact.add_argument("--data", nargs="*", help="Expected data layer files")
    f_impact.add_argument("--di", nargs="*", help="Expected DI files")
    f_impact.add_argument("--tests", nargs="*", help="Expected test files")
    f_impact.add_argument("--config", nargs="*", help="Expected config files")
    f_impact.add_argument("--audit", action="store_true", help="Audit actual git changes against expected scope")

    # sde feature test
    f_test = feat_subs.add_parser("test", help="Run tests for feature using detected profile")
    f_test.add_argument("feature", help="Feature name")

    # sde feature implement
    f_impl = feat_subs.add_parser("implement", help="Display next active TDD implementation task")
    f_impl.add_argument("feature", help="Feature name")

    # sde feature verify
    f_verif = feat_subs.add_parser("verify", help="Run checks and compile verification report with evidence")
    f_verif.add_argument("feature", help="Feature name")

    # sde feature status
    f_status = feat_subs.add_parser("status", help="Show status for a feature")
    f_status.add_argument("feature", nargs="?", help="Feature name")

    # sde profile
    prof_parser = subparsers.add_parser("profile", help="Inspect or list framework profiles")
    prof_parser.add_argument("profile_action", choices=["detect", "list"])

    # sde skill
    skill_parser = subparsers.add_parser("skill", help="Manage and validate agent skills")
    skill_subs = skill_parser.add_subparsers(dest="skill_action", required=True)
    skill_subs.add_parser("validate", help="Validate all skills")
    skill_subs.add_parser("sync", help="Synchronize skills to Claude mirror")
    skill_subs.add_parser("list", help="List installed skills")
    s_new = skill_subs.add_parser("new", help="Scaffold new skill")
    s_new.add_argument("name", help="Skill name")
    s_new.add_argument("--desc", help="Skill description")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
    elif args.command == "doctor":
        cmd_sde_doctor(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "run":
        cmd_sde_run(args)
    elif args.command == "feature":
        if args.feature_action == "create":
            cmd_sde_feature_create(args)
        elif args.feature_action == "specify":
            cmd_specify(args)
        elif args.feature_action == "plan":
            cmd_plan(args)
        elif args.feature_action == "tasks":
            cmd_tasks(args)
        elif args.feature_action == "risk":
            cmd_sde_feature_risk(args)
        elif args.feature_action == "impact":
            cmd_sde_feature_impact(args)
        elif args.feature_action == "test":
            cmd_sde_feature_test(args)
        elif args.feature_action == "implement":
            cmd_sde_feature_implement(args)
        elif args.feature_action == "verify":
            cmd_sde_feature_verify(args)
        elif args.feature_action == "status":
            cmd_status(args)
    elif args.command == "profile":
        cmd_sde_profile(args)
    elif args.command == "skill":
        cmd_sde_skill(args)


if __name__ == "__main__":
    main()
