# GEMINI.md - Google Antigravity Agent Configuration

This workspace utilizes the Antigravity Customization System to equip the agent with structured engineering runbooks following the **SDE (Spec-Driven Engineering)** methodology integrating **[GitHub Spec-Kit](https://github.com/github/spec-kit)**, TDD, Risk-Based HITL, Evidence-Driven Verification, and Framework Profiles.

---

## 1. Discovered Skills
The following skills are installed in `.agents/skills/`:

- **`spec-driven-tdd-engineering`** (`.agents/skills/spec-driven-tdd-engineering/SKILL.md`):
  Enforces SDD, TDD, Risk-based HITL (LOW/MED/HIGH/CRITICAL), Evidence verification, and Framework Profiles.
  *Trigger*: When designing, building, or refactoring components or fixing bugs.
- **`skill-creator`** (`.agents/skills/skill-creator/SKILL.md`):
  Enforces standard authoring, linting, and synchronization of dual-compatible Agent Skills.
  *Trigger*: When the user asks to create or validate a new skill for Claude or AGY.

---

## 2. SDE Workflow & CLI Directives
- **Constitution**: Read `.specify/constitution.md` before starting work.
- **Diagnostics**: Run `python tools/sde.py doctor` to inspect workspace health and detected profiles.
- **Artifact Pipeline**: Use `python tools/sde.py feature {specify, plan, tasks, risk, impact, status}`.
- **Progressive Disclosure**:
  - Do not dump voluminous reference documents into active context unless required by the current step.
  - Follow the relative markdown links within each skill's `SKILL.md` to load specific sub-documentation in `references/`.
  - Use the templates in `templates/` for specs, plans, risks, impacts, and verification reports.

---

## 3. Tool Execution, Risk & Safety
- **Risk-Based Human Gates**: Stop at mandatory gates based on assessed risk (Gate 0 for CRITICAL; Gate 2 for MEDIUM/HIGH/CRITICAL; Gate 3 for HIGH/CRITICAL; Gate 7 for all).
- **Fast-Track Mode**: For LOW risk tasks (cosmetic, minor widgets), execute autonomously and present final evidence at Gate 7.
- **Evidence Integrity**: Never mark `NOT_RUN` as `PASS`. If integration tests or device tests were not executed, record as `N/A` or `NOT_RUN`.
- **Change Impact**: Audit file modifications against `impact.md` via `python tools/sde.py feature impact <name> --audit`.
- Keep `.agents/` and `.claude/` in sync using `python tools/sde.py skill sync`.
