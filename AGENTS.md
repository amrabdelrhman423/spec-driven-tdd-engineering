# AGENTS.md - Workspace Agent Instructions

Welcome to the **SDE (Spec-Driven Engineering) Multi-Agent Workspace**. This repository provides production-grade software engineering skills and tools for AI agents, including **Google Antigravity (AGY)** and **Anthropic Claude (Claude Code)**.

The system integrates the **[GitHub Spec-Kit](https://github.com/github/spec-kit)** specification standard with **Test-Driven Development (TDD)**, **Risk-Based Human-in-the-Loop (HITL)** governance, **Evidence-Driven Verification**, **Change Impact Analysis**, and **Framework Profiles** (Flutter-first).

---

## Available Workspace Skills

| Skill Name | Purpose | Location |
| :--- | :--- | :--- |
| **`spec-driven-tdd-engineering`** | Production AI software engineering system: SDD, TDD, Risk-based HITL, Evidence, Impact Analysis, and Framework Profiles. | [.agents/skills/spec-driven-tdd-engineering/SKILL.md](./.agents/skills/spec-driven-tdd-engineering/SKILL.md) |
| **`skill-creator`** | Author, scaffold, validate, and synchronize portable agent skills. | [.agents/skills/skill-creator/SKILL.md](./.agents/skills/skill-creator/SKILL.md) |

---

## Unified SDE CLI & Workflow

All feature development follows the SDE engineering pipeline:

```bash
# 1. Run environment & repository diagnostic
python tools/sde.py doctor

# 2. Scaffold feature specification & assess risk
python tools/sde.py feature specify <feature-name>
python tools/sde.py feature risk <feature-name> [--level low|medium|high|critical]

# 3. Scaffold technical blueprint & define change scope
python tools/sde.py feature plan <feature-name>
python tools/sde.py feature impact <feature-name> --presentation ... --state ... --tests ...

# 4. Scaffold atomic TDD tasks
python tools/sde.py feature tasks <feature-name>

# 5. Execute TDD cycles (Red -> Green -> Refactor)
# Validate change scope against git diff
python tools/sde.py feature impact <feature-name> --audit

# 6. Check status or run orchestrated pipeline
python tools/sde.py status
python tools/sde.py run <feature-name>
```

*(Legacy aliases `python tools/speckit.py` and `python tools/skill_builder.py` remain fully supported).*

---

## Risk-Based Human-in-the-Loop (HITL) Policy

Autonomous runaway is prohibited on high-consequence changes. Agents dynamically apply human review gates based on assessed risk:

- **`LOW` (Fast Track)**: Cosmetic, text, formatting, safe refactor. No blocking gates between steps. Stop only at **Gate 7 (Final Verification Sign-Off)**.
- **`MEDIUM`**: API integration, state management, DB queries. Requires **Gate 2 (Spec Approval)** and **Gate 7**.
- **`HIGH`**: Payments, security, PII, architecture overhaul. Requires **Gate 2 (Spec)**, **Gate 3 (Plan)**, and **Gate 7**.
- **`CRITICAL`**: Irreversible production data deletion, credentials. Requires **Gate 0 (Pre-Execution Authorization)**.

Protocol reference: [references/human_in_the_loop_protocol.md](./.agents/skills/spec-driven-tdd-engineering/references/human_in_the_loop_protocol.md).

---

## Framework Profiles & Precedence Rule

Agents must inspect and detect the active framework profile via `python tools/sde.py profile detect`.
- **Flutter Profile**: [profiles/flutter/profile.md](./profiles/flutter/profile.md)
- **Precedence Rule**: **Follow repository precedent before introducing personal preference.** (e.g., if project uses Bloc, do not introduce Riverpod; if it uses GetIt, do not introduce manual DI).

---

## Multi-Agent Skill Synchronization

- Synchronize skills between AGY (`.agents/`) and Claude (`.claude/`):
  ```bash
  python tools/sde.py skill sync
  ```
- Validate skill integrity:
  ```bash
  python tools/sde.py skill validate
  ```
