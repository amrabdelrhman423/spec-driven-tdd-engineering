# SDE: Production-Grade AI Software Engineering System

> **A framework-agnostic AI Software Engineering System combining [GitHub Spec-Kit](https://github.com/github/spec-kit) Spec-Driven Development (SDD), Test-Driven Development (TDD), Risk-Based Human-in-the-Loop (HITL) Governance, Evidence-Driven Verification, Change Impact Analysis, and Framework Profiles (Flutter-first).**  
> *Native dual support for [Google Antigravity (AGY)](https://deepmind.google) and [Anthropic Claude (Claude Code)](https://claude.ai).*

---

## Table of Contents

- [1. What is SDE?](#1-what-is-sde)
- [2. The Problem It Solves: Why SDD + TDD?](#2-the-problem-it-solves-why-sdd--tdd)
- [3. GitHub Spec-Kit Relationship](#3-github-spec-kit-relationship)
- [4. The End-to-End Workflow](#4-the-end-to-end-workflow)
- [5. System Architecture: Core vs. Framework Profiles](#5-system-architecture-core-vs-framework-profiles)
- [6. The Flutter Profile (Flutter-First Engineering)](#6-the-flutter-profile-flutter-first-engineering)
- [7. Risk-Based Human-in-the-Loop (HITL) Model](#7-risk-based-human-in-the-loop-hitl-model)
- [8. Change Impact Analysis](#8-change-impact-analysis)
- [9. Evidence-Driven Verification & The Truth Protocol](#9-evidence-driven-verification--the-truth-protocol)
- [10. Unified CLI: `sde`](#10-unified-cli-sde)
- [11. Supported Agent Targets (Claude & Antigravity)](#11-supported-agent-targets-claude--antigravity)
- [12. Complete Reference Example: Flutter Authentication](#12-complete-reference-example-flutter-authentication)
- [13. Fast-Track Workflows](#13-fast-track-workflows)
- [14. Verification & Automated Test Suite](#14-verification--automated-test-suite)
- [15. Roadmap](#15-roadmap)

---

## 1. What is SDE?

**SDE (Spec-Driven Engineering)** evolves AI coding assistants from unconstrained, speculative code generators into disciplined software engineers.

Instead of allowing an AI to guess requirements and write code in a vacuum, SDE enforces a deterministic engineering pipeline:

$$\text{User Intent} \longrightarrow \text{Implementation} + \text{Verification} + \text{Evidence}$$

Every software modification is guided by a formal specification, designed with explicit technical contracts, verified via failing-then-passing tests, audited against an architectural blast radius, and backed by recorded execution logs.

---

## 2. The Problem It Solves: Why SDD + TDD?

When developers use AI coding agents without strict constraints, several failure modes emerge:

| Unconstrained AI Coding ("Vibe Coding") | With the SDE System |
| :--- | :--- |
| ❌ **Autonomous Runaway**: Agent modifies dozens of files without checking in or seeking guidance. | ✅ **Risk-Calibrated HITL**: Agent halts at mandatory gates based on risk (LOW, MEDIUM, HIGH, CRITICAL). |
| ❌ **Hallucinated Requirements & Scope Creep**: Agent guesses domain rules and adds unrequested libraries. | ✅ **Spec-First (SDD)**: Business stories, domain invariants, and out-of-scope non-goals are locked in `spec.md`. |
| ❌ **Brittle Code & Silent Regressions**: Code is written first; tests are written as an afterthought or skipped. | ✅ **Strict TDD (Red $\rightarrow$ Green $\rightarrow$ Refactor)**: Expected assertion failures are witnessed before code is written. |
| ❌ **Untracked Blast Radius**: Agent modifies unrelated files, breaking downstream dependencies. | ✅ **Change Impact Analysis**: Pre-implementation expected scope (`impact.md`) is audited against Git diffs. |
| ❌ **Fake Test Claims**: Agents claim "all tests pass" without executing runners or for missing tests. | ✅ **The Truth Protocol**: Raw output is captured in `evidence/`. Unexecuted suites are strictly marked `N/A` or `NOT_RUN`. |

---

## 3. GitHub Spec-Kit Relationship

SDE does **not** replace [GitHub Spec-Kit](https://github.com/github/spec-kit); it builds upon it as a foundational specification standard.

```text
GitHub Spec-Kit (SDD Foundation)
      │
      ├── Repository Constitution (.specify/constitution.md)
      ├── Specifications (.specify/specs/<feature>/spec.md)
      ├── Technical Plans (.specify/specs/<feature>/plan.md)
      └── Task Breakdowns (.specify/specs/<feature>/tasks.md)
            │
            ▼
SDE AI Engineering System (This Project Adds)
      ├── Strict TDD Lifecycle (Red -> Green -> Refactor)
      ├── Risk Model & Risk-Based HITL Gates (LOW, MED, HIGH, CRITICAL)
      ├── Change Impact Analysis (impact.md & Git Diff Audits)
      ├── Evidence Verification System (verification.md & raw logs)
      ├── The Truth Protocol (Guaranteed genuine test reporting)
      ├── Framework Profiles (Flutter-first, Android, Node, Generic)
      ├── Multi-Agent Runtimes (Google Antigravity & Anthropic Claude)
      ├── Unified CLI Orchestrator (`sde doctor`, `sde run`)
      └── CI/CD Awareness & Deployment Sign-Off
```

---

## 4. The End-to-End Workflow

```text
User Intent
    ↓
Repository Discovery (`sde doctor`)
    ↓
Risk Assessment (`risk.md`)
    ↓
Specification (`spec.md`)  ──> [🚦 Gate 2: Spec Approval]
    ↓
Implementation Plan (`plan.md`) ──> [🚦 Gate 3: Plan Approval (High/Critical)]
    ↓
Change Impact Analysis (`impact.md`)
    ↓
TDD Task Design (`tasks.md`)
    ↓
RED (Failing Test on Domain Assertion)
    ↓
Implementation (Minimal passing code)
    ↓
GREEN (All tests passing)
    ↓
REFACTOR (Clean types, formatting, linting)
    ↓
Impact Audit (Verify actual Git diff matches `impact.md`)
    ↓
Evidence Collection (Write `tests.txt`, `analysis.txt` to `evidence/`)
    ↓
Verification Report (`verification.md`)
    ↓
[🚦 Gate 7: Final Verification & Merge Sign-Off]
    ↓
CI/CD & Deployment
```

---

## 5. System Architecture: Core vs. Framework Profiles

SDE cleanly separates **framework-agnostic engineering logic** from **platform-specific commands and conventions**:

```text
SDE Architecture
│
├── SDE CORE (Framework-Agnostic)
│   ├── SDD Engine (Specifications, Invariants, Acceptance Criteria)
│   ├── TDD Engine (Red-Green-Refactor, Intent Validation)
│   ├── Risk Model (LOW, MEDIUM, HIGH, CRITICAL classification)
│   ├── HITL Protocol (Risk-calibrated human review gates)
│   ├── Evidence System (Truth Protocol, verification.md, raw logs)
│   ├── Change Impact Analyzer (Expected scope vs. Git diff)
│   ├── Diagnostic Doctor (`sde doctor`)
│   └── Workflow Orchestrator (`sde run`)
│
└── FRAMEWORK PROFILES (Platform-Specific)
    ├── Flutter Profile (Dart, Cubit, Riverpod, Provider, GetIt, APK/IPA)
    ├── Android Profile (Kotlin/Java, Gradle, Hilt, JUnit)
    ├── Node.js Profile (JavaScript/TypeScript, npm, Jest, NestJS)
    └── Generic Profile (Agnostic fallback)
```

Each profile encapsulates:
- Dynamic command resolution (e.g. if `integration_test/` does not exist, marks status as `N/A`, never `PASS`).
- Architecture inspection (detects existing conventions from `pubspec.yaml`, `package.json`, etc.).
- Build scripts and lint configurations.

---

## 6. The Flutter Profile (Flutter-First Engineering)

Flutter is the first fully supported, production-grade framework profile.

### Capabilities
- **Static Analysis**: `flutter analyze`
- **Formatting**: `dart format --output=none --set-exit-if-changed .`
- **Unit & Widget Tests**: `flutter test`
- **Integration Tests**: `flutter test integration_test` (conditional)
- **Production Builds**: `flutter build apk`, `flutter build appbundle`, `flutter build ipa --no-codesign`

### Architecture Awareness & The Precedence Rule

> **The Golden Precedence Rule**:  
> **Always follow repository precedent before introducing personal preference.**

The Flutter profile automatically detects existing repository patterns:
- **State Management**: Inspects dependencies for `flutter_bloc` (Bloc/Cubit), `flutter_riverpod` (Riverpod), `provider` (Provider), or `get` (GetX). Never injects a second state management framework if one already exists.
- **Dependency Injection**: Inspects for `get_it` or `injectable`. Registers new dependencies within existing locators.
- **Folder Structure**: Follows Feature-First (`lib/features/<feature>/`) or Layer-First (`lib/presentation/`, `lib/domain/`, etc.).

---

## 7. Risk-Based Human-in-the-Loop (HITL) Model

Instead of requiring 7 manual approvals for a trivial one-line text change, SDE uses a **Risk-Calibrated HITL Model**:

```text
┌──────────────┬──────────────────────────────────────────┬────────────────────────────────────────────┐
│ Tier         │ Typical Scope                            │ Required Human Gates                       │
├──────────────┼──────────────────────────────────────────┼────────────────────────────────────────────┤
│ **LOW**      │ Small UI tweaks, text, formatting, safe  │ **Fast Track**: Spec → Plan → TDD → Verify │
│              │ refactoring, single-widget styling.      │ (Stop only at Gate 7 for Final Sign-Off)   │
├──────────────┼──────────────────────────────────────────┼────────────────────────────────────────────┤
│ **MEDIUM**   │ Standard features, state management, API │ 🚦 Gate 2 (Spec Approval)                  │
│              │ integration, DB queries, local auth.     │ 🚦 Gate 7 (Final Verification Sign-Off)    │
├──────────────┼──────────────────────────────────────────┼────────────────────────────────────────────┤
│ **HIGH**     │ Payments, security, PII, architectural   │ 🚦 Gate 2 (Spec Approval)                  │
│              │ redesign, breaking interface changes.    │ 🚦 Gate 3 (Technical Blueprint Approval)   │
│              │                                          │ 🚦 Gate 7 (Final Verification Sign-Off)    │
├──────────────┼──────────────────────────────────────────┼────────────────────────────────────────────┤
│ **CRITICAL** │ Production DB deletion, credential/key   │ 🚦 Gate 0 (Pre-Execution Authorization)    │
│              │ modification, destructive migration.     │ 🚦 Gates 2, 3, 4, 7 (Strict Sign-off)       │
└──────────────┴──────────────────────────────────────────┴────────────────────────────────────────────┘
```

Every feature receives an assessed `risk.md` artifact detailing:
- Factors: `architecture_change`, `security_sensitive`, `data_migration`, `production_impact`, `breaking_change`, `irreversible_deletion`.
- Rationale explaining why the tier was assigned.

---

## 8. Change Impact Analysis

Before writing implementation code, the agent defines the **Expected Architectural Scope** in `impact.md`:
- Presentation layer (`*.dart`, UI widgets)
- State management (`*.cubit.dart`, `*.bloc.dart`)
- Domain layer (Entities, Repositories, UseCases)
- Data layer (DataSources, DTOs)
- Dependency injection (`injection.dart`)
- Automated tests (`*_test.dart`)
- Configuration (`pubspec.yaml`, `package.json`)

Post-implementation, the CLI audits actual Git modifications against the prediction:
```bash
python tools/sde.py feature impact <feature-name> --audit
```
If unpredicted files are touched, the system outputs:
```text
[FAIL] WARNING: Unexpected Change! The following files were modified outside expected scope:
  * lib/unrelated_payment_engine.dart
```
The agent must document the rationale for the expanded blast radius before proceeding.

---

## 9. Evidence-Driven Verification & The Truth Protocol

In SDE, **no assertion of correctness is accepted without verifiable evidence**.

### The Truth Protocol
- **Never represent `NOT_RUN` as `PASS`.**
- **Never claim a test passed unless the runner executed and exited with code 0.**
- **Never claim integration or device verification occurred if the test was not run.**
- Optional suites that do not exist in the repository (e.g. `integration_test/`) are strictly marked **`N/A`**.

### Standard Verification Artifact (`verification.md`)
Every feature produces a structured `verification.md`:
```markdown
# Verification Report: auth-login
- **Specification Compliance**: PASS
- **Automated Tests**: PASS (Command: `flutter test`, Log: `evidence/tests.txt`)
- **Static Analysis**: PASS (Command: `flutter analyze`, Log: `evidence/analysis.txt`)
- **Build Verification**: PASS (Command: `flutter build apk --debug`)
- **Integration Tests**: N/A (integration_test/ directory absent)
- **Real Device Verification**: NOT_RUN (Scheduled for release staging)
```

---

## 10. Unified CLI: `sde`

The `sde` CLI provides an integrated developer experience:

### Environment Diagnostics
```bash
# Inspect repository readiness (Git, Constitution, Framework, Tests, CI)
python tools/sde.py doctor
```

### Feature Lifecycle
```bash
# 1. Scaffold specification
python tools/sde.py feature specify <feature-name>

# 2. Assess risk
python tools/sde.py feature risk <feature-name> --level medium

# 3. Scaffold technical blueprint
python tools/sde.py feature plan <feature-name>

# 4. Record expected change scope
python tools/sde.py feature impact <feature-name> --presentation ... --state ... --tests ...

# 5. Scaffold TDD tasks
python tools/sde.py feature tasks <feature-name>

# 6. Audit actual Git changes against expected scope
python tools/sde.py feature impact <feature-name> --audit

# 7. Check status
python tools/sde.py status
```

### Full Pipeline Orchestration
```bash
# Orchestrate full pipeline; halts automatically when human approval is required
python tools/sde.py run <feature-name>

# Resume after reviewing and approving a specific gate
python tools/sde.py run <feature-name> --approve "Gate 2: Specification Approval (spec.md)"

# Fast-track override (approves all gates for low-risk changes)
python tools/sde.py run <feature-name> --approve-all
```

### Framework Profiles & Skills
```bash
# Detect active framework profile and conventions
python tools/sde.py profile detect

# List available profiles
python tools/sde.py profile list

# Validate all agent skills
python tools/sde.py skill validate

# Synchronize skills to Claude mirror
python tools/sde.py skill sync
```

*(Legacy commands `python tools/speckit.py` and `python tools/skill_builder.py` remain fully supported).*

---

## 11. Supported Agent Targets (Claude & Antigravity)

SDE maintains dual compatibility with zero vendor lock-in:

### Google Antigravity (AGY)
- **Configuration**: `GEMINI.md` and `AGENTS.md`
- **Skills Location**: `.agents/skills/`
- **Mechanism**: Progressive disclosure via YAML frontmatter triggers.

### Anthropic Claude (Claude Code)
- **Configuration**: `CLAUDE.md` and `AGENTS.md`
- **Skills Location**: `.claude/skills/` (synchronized from `.agents/skills/`)
- **Mechanism**: Terminal execution of `sde` CLI commands.

---

## 12. Complete Reference Example: Flutter Authentication

The repository includes a complete, production-grade Flutter reference implementation:

- **Location**: `.agents/skills/spec-driven-tdd-engineering/examples/flutter_example/`
- **Stack**: Flutter 3.x, Dart 3.x, `flutter_bloc` (Cubit), `get_it` service locator, `mocktail`.
- **Architecture**: Feature-First Clean Architecture (`lib/features/auth/`).
- **Artifacts Included**:
  - [`specs/spec.md`](.agents/skills/spec-driven-tdd-engineering/examples/flutter_example/specs/spec.md): User stories, domain invariants, acceptance criteria.
  - [`specs/plan.md`](.agents/skills/spec-driven-tdd-engineering/examples/flutter_example/specs/plan.md): Mermaid component flow, public interfaces, error matrix.
  - [`specs/risk.md`](.agents/skills/spec-driven-tdd-engineering/examples/flutter_example/specs/risk.md): Assessed `MEDIUM` risk due to authentication credentials.
  - [`specs/impact.md`](.agents/skills/spec-driven-tdd-engineering/examples/flutter_example/specs/impact.md): Expected architectural scope across all layers.
  - [`specs/tasks.md`](.agents/skills/spec-driven-tdd-engineering/examples/flutter_example/specs/tasks.md): Atomic Red-Green-Refactor tasks.
  - [`specs/verification.md`](.agents/skills/spec-driven-tdd-engineering/examples/flutter_example/specs/verification.md): Full verification report with evidence logs.
- **Source Code**:
  - Domain: `lib/features/auth/domain/entities/user.dart`, `lib/features/auth/domain/repositories/auth_repository.dart`
  - Presentation / State: `lib/features/auth/presentation/cubit/login_cubit.dart`, `lib/features/auth/presentation/cubit/login_state.dart`
  - DI Locator: `lib/core/di/injection.dart`
  - Tests: `test/features/auth/presentation/cubit/login_cubit_test.dart`

---

## 13. Fast-Track Workflows

For cosmetic, styling, or minor changes classified as **`LOW` risk**:
1. Run `python tools/sde.py feature specify <name>` to define the single acceptance criterion.
2. Run `python tools/sde.py run <name> --approve-all` or execute the TDD loop directly.
3. The agent does **not** stop for intermediate approvals between Spec, Plan, and Code.
4. The agent presents the verified diff, test output, and `verification.md` at **Gate 7 (Final Sign-Off)**.

---

## 14. Verification & Automated Test Suite

The SDE system itself is thoroughly tested with **41 automated unit tests** covering:
- Risk classification, factor detection, and gate evaluation (`test_risk.py`)
- Evidence collection and Truth Protocol enforcement (`test_evidence.py`)
- Change impact analysis and Git diff auditing (`test_impact.py`)
- Framework profile detection and conditional command resolution (`test_profiles.py`)
- TDD intent validation and failure classification (`test_tdd.py`)
- Diagnostic checks and readiness reporting (`test_doctor.py`)
- Workflow engine and HITL gate blocking (`test_orchestrator.py`)
- SDE CLI commands (`test_sde_cli.py`)
- Spec-Kit and Skill Builder backward compatibility (`test_speckit.py`, `test_skill_builder.py`)

Run the complete test suite:
```bash
python -m unittest discover -s tests
```

---

## 15. Roadmap

- [x] SDE Core (SDD, TDD, Risk-based HITL, Evidence System, Impact Analysis)
- [x] Unified SDE CLI (`sde doctor`, `sde run`, `sde feature`, `sde profile`, `sde skill`)
- [x] Flutter Framework Profile with Cubit/Riverpod/GetIt architecture awareness
- [x] Complete Flutter Authentication reference example
- [x] Android SDK and Node.js Profiles
- [x] CI/CD GitHub Actions Workflow (`.github/workflows/verify.yml`)
- [ ] Golden Toolkit integration for Flutter widget regression testing
- [ ] Native iOS Xcode / Swift Profile
- [ ] Go and Rust Framework Profiles
- [ ] Automated PR description generator compiling `verification.md` into GitHub PR summaries
