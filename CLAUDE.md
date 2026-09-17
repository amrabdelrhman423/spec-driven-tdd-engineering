# CLAUDE.md - Anthropic Claude Project Directives

Welcome to the TDD + SDD workspace. This file instructs Claude Code and Claude-powered agents on workspace capabilities, skills, and coding standards.

This repository implements the **[GitHub Spec-Kit](https://github.com/github/spec-kit)** Spec-Driven Development (SDD) standard.

---

## 1. Available Skills for Claude

Claude skills are located in `.claude/skills/`:

- **`spec-driven-tdd-engineering`** (`.claude/skills/spec-driven-tdd-engineering/SKILL.md`):
  Full workflow for GitHub Spec-Kit Spec-Driven Development (SDD) and Test-Driven Development (TDD).
  - Use when the user asks to implement features, fix issues, or refactor code.
  - Review `references/github_spec_kit_guide.md` for the Spec-Kit artifact pipeline.
  - Review `references/sdd_methodology.md` for spec requirements.
  - Review `references/tdd_lifecycle.md` for the Red-Green-Refactor cycle.
- **`skill-creator`** (`.claude/skills/skill-creator/SKILL.md`):
  Meta-skill to scaffold and validate skills for both Claude and AGY.
  - Use when the user asks to create, modify, or validate an agent skill.

---

## 2. GitHub Spec-Kit SDD Commands

Use `tools/speckit.py` to drive the SDD workflow:
```bash
# Check repository constitution
cat .specify/constitution.md

# Scaffold a new feature specification
python tools/speckit.py specify <feature-name>

# Scaffold a technical blueprint
python tools/speckit.py plan <feature-name>

# Scaffold TDD tasks
python tools/speckit.py tasks <feature-name>

# Check specification and task completion progress
python tools/speckit.py status
```

---

## 3. Skill & Testing CLI Commands

- **Validate all skills**:
  ```bash
  python tools/skill_builder.py validate
  ```
- **Sync skills between agents**:
  ```bash
  python tools/skill_builder.py sync
  ```
- **Scaffold a new skill**:
  ```bash
  python tools/skill_builder.py new <skill_name> --desc "Use this skill when..."
  ```
- **Run Python example tests**:
  ```bash
  python -m unittest discover -s .agents/skills/spec-driven-tdd-engineering/examples/python_example
  ```
- **Run JavaScript example tests**:
  ```bash
  node --test .agents/skills/spec-driven-tdd-engineering/examples/typescript_example/cart_discount.test.js
  ```

---

## 4. Strict Development Guidelines

1. **Constitution First**: Check `.specify/constitution.md` before starting work.
2. **Human Gates (HITL)**: Stop and solicit human review at each of the 7 gates in `spec-driven-tdd-engineering`. Never advance autonomously without explicit approval.
3. **Spec & Plan First (SDD)**: No coding without `spec.md` and `plan.md`. Document requirements, domain invariants, and interfaces.
4. **Always Red First (TDD)**: Write failing tests before writing production code. Confirm they fail for the intended reason.
5. **Keep Implementation Minimal**: Satisfy the tests with the cleanest, simplest logic.
6. **Refactor Safely**: Clean code and types while keeping all tests passing.

