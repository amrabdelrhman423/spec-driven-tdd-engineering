# AGENTS.md - Workspace Agent Instructions

Welcome to the **TDD + SDD Multi-Agent Workspace**. This repository is configured to provide specialized development skills for AI agents, including **Google Antigravity (AGY)** and **Anthropic Claude (Claude Code)**.

The Spec-Driven Development (SDD) methodology in this workspace follows the **[GitHub Spec-Kit](https://github.com/github/spec-kit)** standard.

---

## Available Workspace Skills

| Skill Name | Purpose | Location |
| :--- | :--- | :--- |
| **`spec-driven-tdd-engineering`** | Guides the agent through GitHub Spec-Kit SDD contracts (`constitution.md`, `spec.md`, `plan.md`, `tasks.md`) and TDD Red-Green-Refactor cycles before writing production code. | [.agents/skills/spec-driven-tdd-engineering/SKILL.md](./.agents/skills/spec-driven-tdd-engineering/SKILL.md) |
| **`skill-creator`** | Guides the agent to author, scaffold, validate, and synchronize new dual-compatible skills for Claude and AGY. | [.agents/skills/skill-creator/SKILL.md](./.agents/skills/skill-creator/SKILL.md) |

---

## GitHub Spec-Kit SDD Workflow for Agents

All feature development and major refactoring must follow the **Spec-Kit** pipeline:

1. **Check the Constitution**:
   - Inspect [`.specify/constitution.md`](./.specify/constitution.md) for non-negotiable architectural, security, and testing rules.
2. **Specify & Plan (SDD)**:
   - Scaffold specification: `python tools/speckit.py specify <feature-name>`
   - Scaffold technical blueprint: `python tools/speckit.py plan <feature-name>`
   - Scaffold TDD implementation tasks: `python tools/speckit.py tasks <feature-name>`
3. **Execute via TDD (Red-Green-Refactor)**:
   - **Red**: Write failing tests strictly matching the spec and plan contracts.
   - **Green**: Write the minimal code to satisfy the tests.
   - **Refactor**: Clean code and types without breaking test suites.
4. **Track & Audit**:
   - Check task completion: `python tools/speckit.py status`
   - Validate quality against [checklist template](./.agents/skills/spec-driven-tdd-engineering/templates/speckit_checklist_template.md).

---

## Mandatory Human-in-the-Loop (HITL) Policy

Autonomous runaway is strictly prohibited. All agents must pause and solicit human feedback at each of the **7 Human Review Gates**:
- **Gate 1**: Constitution Alignment & Amendments (before drafting specs)
- **Gate 2**: Specification Approval (`spec.md`)
- **Gate 3**: Technical Blueprint Approval (`plan.md`)
- **Gate 4**: Task Execution Authorization (`tasks.md`)
- **Gate 5**: Failing Test (Red) Approval (per task)
- **Gate 6**: Minimal Implementation & Refactor Approval (per task)
- **Gate 7**: Final Verification & Merge Sign-Off

**Directive**: Halt tool execution, ask targeted design/invariants questions, and await explicit human approval before continuing. Consult [references/human_in_the_loop_protocol.md](./.agents/skills/spec-driven-tdd-engineering/references/human_in_the_loop_protocol.md) for details.

---

## Multi-Agent Skill Synchronization

- Synchronize skills between AGY (`.agents/`) and Claude (`.claude/`):
  ```bash
  python tools/skill_builder.py sync
  ```
- Validate skill integrity:
  ```bash
  python tools/skill_builder.py validate
  ```
