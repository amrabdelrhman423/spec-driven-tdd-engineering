# CLAUDE.md - Anthropic Claude Project Directives

Welcome to the SDE (Spec-Driven Engineering) workspace. This file instructs Claude Code and Claude-powered agents on workspace capabilities, skills, and coding standards.

This repository implements the **SDE Framework** fusing **[GitHub Spec-Kit](https://github.com/github/spec-kit)** Spec-Driven Development (SDD) with Test-Driven Development (TDD), Risk-Based Human-in-the-Loop, Evidence-Driven Verification, and Framework Profiles.

---

## 1. Available Skills for Claude

Claude skills are located in `.claude/skills/`:

- **`spec-driven-tdd-engineering`** (`.claude/skills/spec-driven-tdd-engineering/SKILL.md`):
  Full workflow for SDD, TDD, Risk-based HITL (LOW/MED/HIGH/CRITICAL), Evidence verification, and Framework Profiles.
  - Review `references/human_in_the_loop_protocol.md` for gate triggers.
  - Review `references/evidence_protocol.md` for verification status rules.
  - Review `references/flutter_engineering_guide.md` when operating in Flutter projects.
- **`skill-creator`** (`.claude/skills/skill-creator/SKILL.md`):
  Meta-skill to scaffold, lint, and validate skills for both Claude and AGY.

---

## 2. SDE CLI Commands

Use `tools/sde.py` to drive the workflow:
```bash
# Diagnostic health check
python tools/sde.py doctor

# Feature specification and risk assessment
python tools/sde.py feature specify <feature-name>
python tools/sde.py feature risk <feature-name> --level medium

# Technical blueprint and change scope estimation
python tools/sde.py feature plan <feature-name>
python tools/sde.py feature impact <feature-name> --presentation ... --state ...

# Deconstruct TDD tasks
python tools/sde.py feature tasks <feature-name>

# Post-implementation change scope audit
python tools/sde.py feature impact <feature-name> --audit

# Orchestrate complete pipeline
python tools/sde.py run <feature-name>

# Check status across all features
python tools/sde.py status
```

*(Legacy aliases `python tools/speckit.py` and `python tools/skill_builder.py` remain fully supported).*

---

## 3. Strict Development Guidelines

1. **Constitution First**: Check `.specify/constitution.md` before starting work.
2. **Diagnostic Check**: Run `python tools/sde.py doctor` to verify environment and framework profile.
3. **Risk-Based Human Gates (HITL)**:
   - `LOW`: Fast-track mode enabled; verify autonomously and stop at Gate 7.
   - `MEDIUM`: Stop at Gate 2 (Spec Approval) and Gate 7 (Final Sign-off).
   - `HIGH`: Stop at Gate 2 (Spec), Gate 3 (Plan), and Gate 7.
   - `CRITICAL`: Stop at Gate 0 (Pre-Execution Authorization) before any file is touched.
4. **Follow Repository Precedent**: Follow existing state management, DI, and architecture patterns before introducing personal preference.
5. **Always Red First (TDD)**: Witness expected assertion failure before writing implementation. Infrastructure/syntax errors do not count as RED.
6. **Evidence Integrity**: Record real logs in `evidence/`. Never claim `NOT_RUN` as `PASS`. Record unexecuted optional suites as `N/A`.
