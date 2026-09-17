---
name: spec-driven-tdd-engineering
description: >-
  Use this skill when designing, building, fixing, or refactoring software features using GitHub Spec-Kit Spec-Driven Development (SDD), Test-Driven Development (TDD), risk-based Human-in-the-Loop gates, evidence verification, and framework profiles (Flutter, Android, Node).
---

# Spec-Driven TDD Engineering Skill

This skill guides AI agents through a production-grade engineering workflow combining **[GitHub Spec-Kit](https://github.com/github/spec-kit)** Spec-Driven Development (SDD), **Test-Driven Development (TDD)**, **Risk-Based Human-in-the-Loop (HITL)** governance, **Evidence-Driven Verification**, and **Framework Profiles** (Flutter-first).

---

## 1. Core Workflow Pipeline

```text
User Intent ──> Repo Discovery ──> Risk & Spec ──> Technical Plan ──> Test Design ──> RED ──> GREEN ──> Verify & Evidence ──> CI/CD
```

The agent never acts as a pure code generator; it produces:
$$\text{Implementation} + \text{Verification} + \text{Evidence}$$

---

## 2. Risk-Based Human-in-the-Loop (HITL) Protocol

The agent evaluates task risk into one of four tiers before execution:
- **`LOW` (Fast Track)**: Cosmetic, text, formatting, safe refactoring, minor widgets.
  - *Workflow*: Spec $\rightarrow$ Plan $\rightarrow$ TDD $\rightarrow$ Verify. No blocking gates between steps. Stop only at **Gate 7 (Final Sign-off)**.
- **`MEDIUM`**: API integration, state management, database queries, local authentication.
  - *Workflow*: Requires **Gate 2 (Spec Approval)** before technical planning, plus **Gate 7**.
- **`HIGH`**: Payments, security, PII, architectural redesign, breaking API changes.
  - *Workflow*: Requires **Gate 2 (Spec)**, **Gate 3 (Plan)**, and **Gate 7**.
- **`CRITICAL`**: Irreversible production data deletion, credential modification.
  - *Workflow*: Requires **Gate 0 (Pre-Execution Authorization)** prior to modifying any file.

> [!CAUTION]
> Autonomous runaway on HIGH and CRITICAL tasks is strictly forbidden. The agent MUST stop tool execution and await explicit human approval.
> Detailed protocol: [references/human_in_the_loop_protocol.md](./references/human_in_the_loop_protocol.md) | [references/risk_assessment_guide.md](./references/risk_assessment_guide.md)

---

## 3. Engineering Stages

### Stage 1: Repository Discovery & Constitution Alignment
1. Inspect `.specify/constitution.md` for architectural, testing, and security non-negotiables.
2. Run `python tools/sde.py doctor` to verify repository readiness and detected framework profiles.
3. If CRITICAL risk: Halt for **Gate 0 Pre-Execution Authorization**.

### Stage 2: Spec-Driven Development (Specify & Plan)
1. **Scaffold Specification (`spec.md`)**:
   - Run: `python tools/sde.py feature specify <feature-name>`
   - Define User Stories, Domain Invariants, and Given-When-Then Acceptance Criteria.
   - Assess Risk: `python tools/sde.py feature risk <feature-name> [--level / flags]`
   - If MEDIUM, HIGH, or CRITICAL: Halt for **🚦 Gate 2: Specification Approval**.
2. **Draft Technical Blueprint (`plan.md`)**:
   - Run: `python tools/sde.py feature plan <feature-name>`
   - Document Component Flow, File Structure, Public Interfaces, and Error Matrix.
   - If HIGH or CRITICAL: Halt for **🚦 Gate 3: Technical Blueprint Approval**.
3. **Pre-Implementation Change Impact Analysis (`impact.md`)**:
   - Run: `python tools/sde.py feature impact <feature-name> --presentation ... --state ... --tests ...`
   - Capture expected architectural blast radius: [references/change_impact_analysis.md](./references/change_impact_analysis.md).
4. **Deconstruct TDD Tasks (`tasks.md`)**:
   - Run: `python tools/sde.py feature tasks <feature-name>`

### Stage 3: Test-Driven Development (TDD) Loop (Red -> Green -> Refactor)
1. **RED (Write Failing Test)**:
   - State explicit **Test Intent**: What behavior does this test prove? Why should it fail before implementation?
   - Execute test runner (`flutter test`, `npm test`, `python -m unittest`).
   - Confirm an **Assertion Failure** (valid RED). Syntax, missing imports, or missing runner are **Infrastructure Failures**, not valid RED.
2. **GREEN (Minimal Implementation)**:
   - Author minimal production code to make the test pass. No speculative logic.
3. **REFACTOR (Polish Under Test Protection)**:
   - Format, clean code, verify strict typing, run linters.
   - Re-run test suite to ensure zero regressions: [references/tdd_lifecycle.md](./references/tdd_lifecycle.md).
4. **Audit Change Scope**:
   - Run `python tools/sde.py feature impact <feature-name> --audit`. If unexpected files were touched, analyze before continuing.

### Stage 4: Evidence-Driven Verification & Sign-Off
1. **Execute Quality Checks & Record Evidence**:
   - Run static analysis and unit/widget test suites.
   - Collect raw outputs into `.specify/specs/<feature-name>/evidence/`.
   - Update `.specify/specs/<feature-name>/verification.md`: [references/evidence_protocol.md](./references/evidence_protocol.md).
2. **Status Rules**:
   - Use strictly: `PASS`, `FAIL`, `NOT_RUN`, `BLOCKED`, `N/A`.
   - Never represent `NOT_RUN` as `PASS`. Missing optional suites (e.g. `integration_test/`) are marked `N/A`.
3. **Final Sign-Off**:
   - **🚦 Gate 7: Final Verification & Merge Sign-Off**. Present test results, evidence logs, and checklist summary for human authorization.

---

## 4. Framework Profiles

SDE dynamically configures itself according to the repository's technology profile:
- **Flutter Profile** (`profiles/flutter/`): Full support for Dart, Bloc/Cubit, Riverpod, Provider, GetIt, unit tests, widget tests, integration tests, and apk/appbundle/ipa builds. Follows repository precedent: [references/flutter_engineering_guide.md](./references/flutter_engineering_guide.md).
- **Android Profile** (`profiles/android/`): Native Kotlin/Java Gradle lifecycle.
- **Node.js Profile** (`profiles/node/`): JS/TS testing, linting, and build pipeline.
- Profile Guide: [references/framework_profiles_guide.md](./references/framework_profiles_guide.md).

---

## 5. Reference Guides & Templates

| Category | Document | Description |
| :--- | :--- | :--- |
| **Protocol** | [references/human_in_the_loop_protocol.md](./references/human_in_the_loop_protocol.md) | Risk-based HITL gate triggers, responses & fast-track |
| **Protocol** | [references/risk_assessment_guide.md](./references/risk_assessment_guide.md) | Risk tier taxonomy and factor definitions |
| **Protocol** | [references/evidence_protocol.md](./references/evidence_protocol.md) | Evidence collection and verification status rules |
| **Protocol** | [references/change_impact_analysis.md](./references/change_impact_analysis.md) | Blast radius prediction and git diff audits |
| **Framework** | [references/flutter_engineering_guide.md](./references/flutter_engineering_guide.md) | Flutter TDD, architecture inspection, and testing |
| **Framework** | [references/framework_profiles_guide.md](./references/framework_profiles_guide.md) | Profile architecture and command resolution |
| **SDD/TDD** | [references/sdd_methodology.md](./references/sdd_methodology.md) | Spec-Driven Development deep dive |
| **SDD/TDD** | [references/tdd_lifecycle.md](./references/tdd_lifecycle.md) | Red-Green-Refactor mechanics and anti-patterns |
| **Templates** | [templates/risk_template.md](./templates/risk_template.md) | Risk assessment template (`risk.md`) |
| **Templates** | [templates/impact_template.md](./templates/impact_template.md) | Expected architectural scope template (`impact.md`) |
| **Templates** | [templates/verification_template.md](./templates/verification_template.md) | Evidence-driven verification template (`verification.md`) |
| **Templates** | [templates/speckit_specification_template.md](./templates/speckit_specification_template.md) | Specification template (`spec.md`) |
| **Templates** | [templates/speckit_plan_template.md](./templates/speckit_plan_template.md) | Technical blueprint template (`plan.md`) |
| **Templates** | [templates/speckit_tasks_template.md](./templates/speckit_tasks_template.md) | TDD task checklist template (`tasks.md`) |
| **Templates** | [templates/speckit_checklist_template.md](./templates/speckit_checklist_template.md) | Final quality audit checklist (`checklist.md`) |
