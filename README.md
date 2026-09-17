# Universal Agent Skills for Claude & Google Antigravity (AGY)

> **A production-grade system and reference architecture for authoring, validating, and executing portable Agent Skills across [Google Antigravity (AGY)](https://deepmind.google) and [Anthropic Claude (Claude Code)](https://claude.ai).**

---

## Table of Contents

- [Overview](#overview)
- [The Core Skill: `spec-driven-tdd-engineering`](#the-core-skill-spec-driven-tdd-engineering)
  - [What is it?](#what-is-it)
  - [What Problem Does It Solve?](#what-problem-does-it-solve)
  - [The 4-Stage Pipeline](#the-4-stage-pipeline)
  - [The 7 Mandatory Human Review Gates](#the-7-mandatory-human-review-gates)
- [How to Use It: Step-by-Step Guide](#how-to-use-it-step-by-step-guide)
  - [Step 1: Check Constitution (Gate 1)](#step-1-check-constitution-gate-1)
  - [Step 2: Scaffold & Approve Specification (Gate 2)](#step-2-scaffold--approve-specification-gate-2)
  - [Step 3: Draft & Approve Technical Blueprint (Gate 3)](#step-3-draft--approve-technical-blueprint-gate-3)
  - [Step 4: Generate & Authorize TDD Tasks (Gate 4)](#step-4-generate--authorize-tdd-tasks-gate-4)
  - [Step 5: Execute TDD Cycles (Gates 5 & 6)](#step-5-execute-tdd-cycles-gates-5--6)
  - [Step 6: Audit & Merge Sign-Off (Gate 7)](#step-6-audit--merge-sign-off-gate-7)
- [Architecture & Cross-Agent Portability](#architecture--cross-agent-portability)
  - [Repository Layout](#repository-layout)
  - [How Google Antigravity (AGY) Loads Skills](#how-google-antigravity-agy-loads-skills)
  - [How Anthropic Claude Loads Skills](#how-anthropic-claude-loads-skills)
- [CLI Tooling](#cli-tooling)
  - [1. GitHub Spec-Kit CLI (`tools/speckit.py`)](#1-github-spec-kit-cli-toolsspeckitpy)
  - [2. Multi-Agent Skill Builder (`tools/skill_builder.py`)](#2-multi-agent-skill-builder-toolsskill_builderpy)
- [Included Reference Implementations](#included-reference-implementations)
- [Verification & Automated Test Suite](#verification--automated-test-suite)

---

## Overview

Modern AI coding agents are exceptionally capable at generating code quickly, but unrestricted autonomy often leads to **"vibe coding"**, architectural drift, hallucinations, and breaking changes. 

This repository provides an end-to-end framework solving this problem through:
1. **`spec-driven-tdd-engineering` Skill**: A disciplined engineering workflow fusing **[GitHub Spec-Kit](https://github.com/github/spec-kit)** Spec-Driven Development (SDD) with **Test-Driven Development (TDD)** and **Human-in-the-Loop (HITL)** checkpoints.
2. **`skill-creator` Meta-Skill & Tooling**: An automated CLI tool (`tools/skill_builder.py`) to scaffold, lint, validate link integrity, and keep dual `.agents/` and `.claude/` skill directories in sync.
3. **Dual Agent Runtime Portability**: Out-of-the-box support for **Google Antigravity** (`.agents/skills/`, `AGENTS.md`, `GEMINI.md`) and **Anthropic Claude** (`.claude/skills/`, `CLAUDE.md`).

---

## The Core Skill: `spec-driven-tdd-engineering`

### What is it?

`spec-driven-tdd-engineering` is an **Agent Skill** designed to transform AI coding assistants from unchecked code generators into rigorous software engineers. It standardizes the development process around four non-negotiable artifacts:
- **`constitution.md`**: Foundational repository covenants, security boundaries, and architectural rules.
- **`spec.md`**: Business context, user stories, acceptance criteria, and non-negotiable domain invariants.
- **`plan.md`**: Technical blueprints, component interfaces, data contracts, and failure matrices.
- **`tasks.md`**: Atomic, ordered Red-Green-Refactor test tasks.

### What Problem Does It Solve?

| Traditional AI Coding ("Vibe Coding") | With `spec-driven-tdd-engineering` |
| :--- | :--- |
| ❌ **Autonomous Runaway**: Agent churns out hundreds of lines without checking in. | ✅ **7 Human Review Gates**: Agent stops at critical checkpoints and awaits explicit human approval. |
| ❌ **Hallucinated Requirements**: Agent guesses business rules and edge cases. | ✅ **Spec-First Contracts**: Formal user stories and domain invariants in `spec.md` prevent ambiguity. |
| ❌ **Untested Code & Regressions**: Code is written first; tests are written as an afterthought (or never). | ✅ **Strict TDD (Red -> Green -> Refactor)**: Failing tests are authored and witnessed before implementation code. |
| ❌ **Over-Engineering & Speculation**: Agent adds unrequested libraries, features, or abstractions. | ✅ **Constitutional & Minimalist Enforcement**: Agent writes only the minimal code to satisfy failing tests. |
| ❌ **Platform Lock-In**: Skills written for one LLM tool fail on others. | ✅ **Universal Dual Compatibility**: Fully portable across Google Antigravity and Anthropic Claude. |

---

### The 4-Stage Pipeline

```text
┌────────────────────────────────────────────────────────────────────────┐
│  STAGE 1: CONSTITUTION CHECK                                           │
│  Agent verifies repository principles in constitution.md               │
│  🚦 GATE 1: Constitution Alignment & Amendments                       │
├────────────────────────────────────────────────────────────────────────┤
│  STAGE 2a: SPECIFICATION (spec.md)                                     │
│  Agent defines user stories, invariants, acceptance criteria           │
│  🚦 GATE 2: Specification Approval                                     │
├────────────────────────────────────────────────────────────────────────┤
│  STAGE 2b: TECHNICAL PLAN (plan.md)                                    │
│  Agent designs architecture, interfaces, and error matrix              │
│  🚦 GATE 3: Technical Blueprint & Contract Approval                    │
├────────────────────────────────────────────────────────────────────────┤
│  STAGE 2c: TASK BREAKDOWN (tasks.md)                                   │
│  Agent decomposes plan into atomic TDD Red-Green-Refactor tasks        │
│  🚦 GATE 4: Task Execution Authorization                               │
├────────────────────────────────────────────────────────────────────────┤
│  STAGE 3: TDD IMPLEMENTATION LOOP (Per Task)                           │
│  Agent authors failing test, executes, confirms failure                │
│  🚦 GATE 5: Failing Test (Red) Approval                                │
│  Agent implements minimal code, refactors, confirms all pass           │
│  🚦 GATE 6: Minimal Code & Refactor (Green) Approval                   │
├────────────────────────────────────────────────────────────────────────┤
│  STAGE 4: FINAL AUDIT & DELIVERY                                       │
│  Agent runs full suite, verifies invariants, audits checklist          │
│  🚦 GATE 7: Final Verification & Merge Sign-Off                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

### The 7 Mandatory Human Review Gates

Autonomous execution past gates is strictly forbidden. At each gate, the agent halts and prompts the user:

1. **🚦 Gate 1: Constitution Alignment & Amendments**
   - *When*: Before scaffolding any feature.
   - *Prompt*: *"I have reviewed `.specify/constitution.md`. Constraints governing this work are: [summary]. Do these apply as written, or are amendments needed?"*
2. **🚦 Gate 2: Specification Approval (`spec.md`)**
   - *When*: After drafting the specification.
   - *Prompt*: *"Please review the specification draft. Are domain invariants correct? Any missing acceptance criteria or edge cases? Do you approve this specification?"*
3. **🚦 Gate 3: Technical Blueprint & Contract Approval (`plan.md`)**
   - *When*: After drafting the technical architecture.
   - *Prompt*: *"Please review the technical plan. Do the public interface signatures and data models meet your requirements? Is the error matrix complete? Do you approve this blueprint?"*
4. **🚦 Gate 4: Task Execution Authorization (`tasks.md`)**
   - *When*: After breaking the plan into atomic TDD tasks.
   - *Prompt*: *"Here is the TDD task breakdown. Is the task ordering and scope appropriate? Do you authorize beginning TDD execution on Phase 1?"*
5. **🚦 Gate 5: Failing Test (Red) Approval**
   - *When*: Per-task, after writing the test and confirming it fails.
   - *Prompt*: *"Task [X.Y] (RED): Test fails with [assertion error]. Do you approve this test contract before I write the minimal implementation?"*
6. **🚦 Gate 6: Minimal Implementation & Refactor (Green) Approval**
   - *When*: Per-task, after writing minimal code and passing tests.
   - *Prompt*: *"Task [X.Y] (GREEN & REFACTOR): All tests pass cleanly. Refactorings: [summary]. Do you approve this implementation to mark Task [X.Y] complete and move to the next task?"*
7. **🚦 Gate 7: Final Verification & Merge Sign-Off**
   - *When*: After all tasks and quality checklists pass 100%.
   - *Prompt*: *"All tasks complete, 100% tests pass, checklist satisfied. Do you give final approval to merge / finalize this feature?"*

> [!NOTE]
> For complete protocol mechanics, approval keywords, revision loops, and fast-track rules, see [references/human_in_the_loop_protocol.md](.agents/skills/spec-driven-tdd-engineering/references/human_in_the_loop_protocol.md).

---

## How to Use It: Step-by-Step Guide

Whether you are prompting an agent in **Antigravity IDE** or **Claude Code**, here is the standard workflow:

### Step 1: Check Constitution (Gate 1)
Verify repository covenants before planning:
```bash
# Read existing repository constitution
cat .specify/constitution.md

# Or initialize a new constitution if starting a fresh repo
python tools/speckit.py init
```
*Agent halts at **Gate 1** to confirm constitutional rules with the developer.*

### Step 2: Scaffold & Approve Specification (Gate 2)
Scaffold the feature specification:
```bash
python tools/speckit.py specify payment-gateway
```
- The agent populates `.specify/specs/payment-gateway/spec.md` using [speckit_specification_template.md](.agents/skills/spec-driven-tdd-engineering/templates/speckit_specification_template.md).
- Documents: Problem Statement, User Stories, In-Scope / Out-of-Scope, Domain Invariants, Given-When-Then criteria.
*Agent halts at **Gate 2** to solicit human approval of requirements and domain invariants.*

### Step 3: Draft & Approve Technical Blueprint (Gate 3)
Scaffold the technical plan:
```bash
python tools/speckit.py plan payment-gateway
```
- The agent populates `.specify/specs/payment-gateway/plan.md` using [speckit_plan_template.md](.agents/skills/spec-driven-tdd-engineering/templates/speckit_plan_template.md).
- Documents: Architecture diagram, module layout, public contracts, and error handling matrix.
*Agent halts at **Gate 3** to verify signatures and error handling with the developer.*

### Step 4: Generate & Authorize TDD Tasks (Gate 4)
Generate the atomic task checklist:
```bash
python tools/speckit.py tasks payment-gateway
```
- Populates `.specify/specs/payment-gateway/tasks.md` with structured Red/Green/Refactor task items.
*Agent halts at **Gate 4** to authorize starting code execution.*

### Step 5: Execute TDD Cycles (Gates 5 & 6)
For each task in `tasks.md`:
1. **Red**: Agent writes test -> runs runner -> test fails -> **Gate 5 (Human verifies test & failure mode)**.
2. **Green**: Agent writes minimal passing code -> runs runner -> all tests pass.
3. **Refactor**: Agent cleans code, fixes types, runs linters -> tests still pass -> **Gate 6 (Human approves implementation)**.

Track real-time progress:
```bash
python tools/speckit.py status
```

### Step 6: Audit & Merge Sign-Off (Gate 7)
Run static analysis, type checks, and complete the quality audit:
```bash
# Verify unit tests
python -m unittest discover -s tests

# Audit Spec-Kit checklist
cat .specify/specs/payment-gateway/checklist.md
```
*Agent halts at **Gate 7** for final human authorization to merge or release.*

---

## Architecture & Cross-Agent Portability

### Repository Layout

```text
├── AGENTS.md                          # Universal agent directives & HITL policy
├── GEMINI.md                          # Google Antigravity specific configuration
├── CLAUDE.md                          # Anthropic Claude Code commands & guidelines
├── .specify/                          # Spec-Kit directory
│   ├── constitution.md                # Non-negotiable repository covenants (Article I-V)
│   └── specs/                         # Feature specifications, plans, and tasks
├── .agents/skills/                    # Primary skill discovery root (AGY)
│   ├── spec-driven-tdd-engineering/   # The TDD + SDD Engineering Skill
│   │   ├── SKILL.md                   # Main runbook with frontmatter & 7 Human Gates
│   │   ├── references/                # In-depth theory & protocol guides
│   │   ├── templates/                 # Spec, plan, task, and checklist templates
│   │   └── examples/                  # Reference Python & TypeScript projects
│   └── skill-creator/                 # Meta-skill for authoring new agent skills
├── .claude/skills/                    # Synchronized Claude mirror
├── tools/
│   ├── speckit.py                     # GitHub Spec-Kit workflow CLI
│   └── skill_builder.py               # Skill validation, scaffolding, & sync CLI
└── tests/                             # Unit tests for CLI tools and validators
```

### How Google Antigravity (AGY) Loads Skills
- AGY discovers skills from `.agents/skills/<skill_name>/SKILL.md`.
- **Progressive Disclosure**: Only the `name` and `description` from the YAML frontmatter are injected into the agent prompt initially.
- When triggered by a coding task, AGY reads `SKILL.md` and loads linked references in `references/` on demand.

### How Anthropic Claude Loads Skills
- Claude reads directives from `CLAUDE.md`.
- Claude discovers mirrored skills under `.claude/skills/<skill_name>/SKILL.md`.
- Claude follows progressive links and executes CLI commands.

---

## CLI Tooling

### 1. GitHub Spec-Kit CLI (`tools/speckit.py`)

Driven by the [GitHub Spec-Kit](https://github.com/github/spec-kit) standard, this script manages the SDD artifact lifecycle:

```bash
# 1. Initialize repository constitution (.specify/constitution.md)
python tools/speckit.py init

# 2. Scaffold a new feature specification
python tools/speckit.py specify <feature-name>

# 3. Scaffold technical blueprint
python tools/speckit.py plan <feature-name>

# 4. Scaffold TDD implementation tasks
python tools/speckit.py tasks <feature-name>

# 5. Check completion status across all features
python tools/speckit.py status
```

### 2. Multi-Agent Skill Builder (`tools/skill_builder.py`)

CLI utility to validate, scaffold, and sync skills across both agent runtimes:

```bash
# 1. Validate all skills (frontmatter, <500 lines threshold, markdown link integrity)
python tools/skill_builder.py validate

# 2. Synchronize skills from .agents/ to .claude/
python tools/skill_builder.py sync

# 3. Scaffold a new custom skill
python tools/skill_builder.py new <skill-name> --desc "Use this skill when..."

# 4. List installed skills
python tools/skill_builder.py list
```

---

## Included Reference Implementations

The workspace includes complete, working reference implementations built using the `spec-driven-tdd-engineering` skill:

### 1. Python: E-Commerce Order Processor
- **Location**: `.agents/skills/spec-driven-tdd-engineering/examples/python_example/`
- **Features**: State machine transitions (`PENDING -> PAID -> SHIPPED`), domain invariant enforcement, isolated unit tests.
- **Run Tests**:
  ```bash
  python -m unittest discover -s .agents/skills/spec-driven-tdd-engineering/examples/python_example
  ```

### 2. JavaScript / TypeScript: Shopping Cart Discount Engine
- **Location**: `.agents/skills/spec-driven-tdd-engineering/examples/typescript_example/`
- **Features**: Percentage & fixed coupons, free shipping calculation, invariant boundary guards.
- **Run Tests**:
  ```bash
  node --test .agents/skills/spec-driven-tdd-engineering/examples/typescript_example/cart_discount.test.js
  ```

---

## Verification & Automated Test Suite

To verify workspace integrity, link validity, and tool functionality, run the unit test suite:

```bash
python -m unittest discover -s tests
```

**Test Coverage Summary**:
- `test_skill_builder.py`: Validates YAML frontmatter parsing, progressive disclosure limits, relative link resolution, and file synchronization.
- `test_speckit.py`: Validates feature scaffolding (`specify`, `plan`, `tasks`), constitution initialization, and status reporting.

---

## Documentation Index

| Guide | Purpose |
| :--- | :--- |
| [human_in_the_loop_protocol.md](.agents/skills/spec-driven-tdd-engineering/references/human_in_the_loop_protocol.md) | **HITL philosophy, 7 gate triggers, approval keywords, and revision loops** |
| [github_spec_kit_guide.md](.agents/skills/spec-driven-tdd-engineering/references/github_spec_kit_guide.md) | GitHub Spec-Kit artifact hierarchy and lifecycle |
| [sdd_methodology.md](.agents/skills/spec-driven-tdd-engineering/references/sdd_methodology.md) | Spec-Driven Development deep dive |
| [tdd_lifecycle.md](.agents/skills/spec-driven-tdd-engineering/references/tdd_lifecycle.md) | Red-Green-Refactor mechanics and anti-patterns |
| [invariant_and_property_testing.md](.agents/skills/spec-driven-tdd-engineering/references/invariant_and_property_testing.md) | Invariants and property-based testing guide |
| [test_doubles_and_mocking.md](.agents/skills/spec-driven-tdd-engineering/references/test_doubles_and_mocking.md) | In-memory fakes vs. mocks best practices |
| [claude_vs_agy.md](.agents/skills/skill-creator/references/claude_vs_agy.md) | Architectural comparison of Claude Code vs. Google Antigravity |
| [progressive_disclosure.md](.agents/skills/skill-creator/references/progressive_disclosure.md) | Token economy and progressive disclosure rules |
