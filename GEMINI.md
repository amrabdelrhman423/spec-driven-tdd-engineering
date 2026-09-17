# GEMINI.md - Google Antigravity Agent Configuration

This workspace utilizes the Antigravity Customization System to equip the agent with structured engineering runbooks following the **[GitHub Spec-Kit](https://github.com/github/spec-kit)** Spec-Driven Development (SDD) standard.

---

## 1. Discovered Skills
The following skills are installed in `.agents/skills/`:

- **`spec-driven-tdd-engineering`** (`.agents/skills/spec-driven-tdd-engineering/SKILL.md`):
  Enforces GitHub Spec-Kit Spec-Driven Development (SDD) and Test-Driven Development (TDD).
  *Trigger*: When designing, building, or refactoring components or fixing bugs.
- **`skill-creator`** (`.agents/skills/skill-creator/SKILL.md`):
  Enforces standard authoring, linting, and synchronization of dual-compatible Agent Skills.
  *Trigger*: When the user asks to create or validate a new skill for Claude or AGY.

---

## 2. GitHub Spec-Kit SDD Directives
- **Constitution**: Always read `.specify/constitution.md` before starting work.
- **Artifact Pipeline**: Use `python tools/speckit.py {specify, plan, tasks, status}` to manage specifications and technical plans.
- **Progressive Disclosure**:
  - Do not dump voluminous reference documents into active context unless required by the current step.
  - Follow the relative markdown links within each skill's `SKILL.md` to load specific sub-documentation in `references/`.
  - Use the templates in `templates/` for specs, plans, test matrices, and verification checklists.

---

## 3. Tool Execution & Safety
- **Mandatory Human Gates**: Before proceeding past any `🚦 HUMAN GATE` (Gates 1–7) in `spec-driven-tdd-engineering`, stop tool calls and ask the human for approval. Autonomous execution past gates is forbidden.
- Run automated tests after modifying code.
- Verify tests fail (Red) before writing implementation code (Green).
- Keep `.agents/` and `.claude/` in sync using `python tools/skill_builder.py sync`.

