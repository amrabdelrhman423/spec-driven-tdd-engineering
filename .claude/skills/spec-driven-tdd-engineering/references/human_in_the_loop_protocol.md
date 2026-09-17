# Risk-Based Human-in-the-Loop (HITL) Protocol

This document establishes the official Human-in-the-Loop engineering protocol for the `spec-driven-tdd-engineering` skill. It governs how AI agents interact with human engineers across every stage of Spec-Driven Development (SDD) and Test-Driven Development (TDD).

---

## 1. Core Philosophy: Trust, Verify & Risk-Calibrated Autonomy

In an autonomous or semi-autonomous development environment, agentic models excel at synthesizing code, generating test cases, and exploring edge conditions. However:
- Agents lack real-world business context and organizational history.
- Unchecked autonomy can lead to hallucinated requirements, speculative architecture ("vibe coding"), and silent regressions.
- Overly rigid human gates on trivial changes cause fatigue and friction.

**The Solution: Risk-Calibrated Human-in-the-Loop.**
The system dynamically scales human oversight based on the blast radius and architectural risk of the change.

---

## 2. The 4 Risk Tiers & Gate Triggers

```text
┌──────────────┬──────────────────────────────────────────┬────────────────────────────────────────────┐
│ Tier         │ Typical Changes                          │ Mandatory Gate Checkpoints                 │
├──────────────┼──────────────────────────────────────────┼────────────────────────────────────────────┤
│ **LOW**      │ Small UI tweaks, text, formatting, safe  │ **Fast Track**: Spec → Plan → TDD → Verify │
│              │ refactoring, single-widget styling.      │ (Final Gate 7 verification only)           │
├──────────────┼──────────────────────────────────────────┼────────────────────────────────────────────┤
│ **MEDIUM**   │ Standard features, state management, API │ 🚦 Gate 2 (Spec Approval)                  │
│              │ consumption, DB queries, local auth.     │ 🚦 Gate 7 (Final Verification & Sign-off)  │
├──────────────┼──────────────────────────────────────────┼────────────────────────────────────────────┤
│ **HIGH**     │ Payments, security, PII, architectural   │ 🚦 Gate 2 (Spec Approval)                  │
│              │ redesign, breaking interface changes.    │ 🚦 Gate 3 (Technical Blueprint Approval)   │
│              │                                          │ 🚦 Gate 7 (Final Verification & Sign-off)  │
├──────────────┼──────────────────────────────────────────┼────────────────────────────────────────────┤
│ **CRITICAL** │ Production DB deletion, credential/key   │ 🚦 Gate 0 (Pre-Execution Authorization)    │
│              │ modification, destructive migration.     │ 🚦 Gates 2, 3, 4, 7 (Full Multi-Signature) │
└──────────────┴──────────────────────────────────────────┴────────────────────────────────────────────┘
```

---

## 3. The 7 Engineering Gates Detailed

### Gate 0: Pre-Execution Authorization (CRITICAL Only)
- **Trigger**: Prior to touching any files when risk factors indicate irreversible deletion or production credential modification.
- **Mandatory Agent Prompt**:
  > *"CRITICAL OPERATION DETECTED: [summary]. Explicit human authorization is mandatory before any execution begins. Do you authorize proceeding with this specification?"*
- **Wait Condition**: STOP and await human response.

### Gate 1: Constitution Alignment Gate
- **Trigger**: When beginning work on a new repository or major architectural subsystem.
- **Agent Action**: Verify `.specify/constitution.md` covenants.

### Gate 2: Specification Approval Gate (`spec.md`)
- **Trigger**: Immediately after drafting `.specify/specs/<feature>/spec.md` (Medium, High, Critical).
- **Mandatory Agent Prompt**:
  > *"Please review the specification draft for `[feature-name]`. Are domain invariants correct? Are there any missing acceptance criteria or edge cases? Do you approve this specification?"*

### Gate 3: Technical Blueprint & Contract Approval Gate (`plan.md`)
- **Trigger**: Immediately after drafting `.specify/specs/<feature>/plan.md` (High, Critical).
- **Mandatory Agent Prompt**:
  > *"Please review the technical plan. Do public interface signatures and data models meet your requirements? Is the error matrix complete? Do you approve this blueprint?"*

### Gate 4: Task Execution Authorization Gate (`tasks.md`)
- **Trigger**: Immediately after generating `.specify/specs/<feature>/tasks.md` (Critical or upon request).
- **Mandatory Agent Prompt**:
  > *"Here is the TDD task breakdown. Is the task ordering and scope appropriate? Do you authorize beginning TDD execution?"*

### Gate 5: Failing Test (Red) Approval Gate (Per-Task)
- **Trigger**: After running failing test in High-Oversight mode.
- **Mandatory Agent Prompt**:
  > *"Task [X.Y] (RED): Test fails as expected with [assertion error]. Approve this test before I write the minimal implementation?"*

### Gate 6: Minimal Code & Refactor (Green) Approval Gate (Per-Task)
- **Trigger**: After minimal code passes tests in High-Oversight mode.
- **Mandatory Agent Prompt**:
  > *"Task [X.Y] (GREEN & REFACTOR): All tests pass cleanly. Refactorings: [summary]. Approve to move to the next task?"*

### Gate 7: Final Verification & Merge Sign-Off Gate (ALL Tiers)
- **Trigger**: After all tasks are completed, static analysis passes, and `verification.md` is compiled.
- **Mandatory Agent Prompt**:
  > *"All tasks complete, 100% tests pass, and evidence is recorded in `verification.md`. Do you give final approval to merge / finalize this feature?"*

---

## 4. Human Feedback & Revision Protocol

- **Approval**: `"approved"`, `"proceed"`, `"yes"`, `"lgtm"`, `"continue"`, `"ship it"` $\rightarrow$ Advance to the next stage.
- **Revision Request**: The agent incorporates modifications into the artifact (spec, plan, code) and re-presents at the **same gate**.
- **Clarification**: Provide technical explanation and re-ask the approval question.

---

## 5. Escalation Rules: When to Stop Immediately

Stop immediately and ask for guidance if:
1. **Architectural Contradiction**: Conflict with `.specify/constitution.md`.
2. **Unexpected Change Scope**: Git diff touches files outside the pre-approved `impact.md` scope.
3. **Infrastructure Failure vs. Red Failure**: Test failure is caused by a syntax error or missing runner rather than an assertion failure.
4. **Third-Party Dependency Addition**: Introducing new packages not already in the repository manifest.
