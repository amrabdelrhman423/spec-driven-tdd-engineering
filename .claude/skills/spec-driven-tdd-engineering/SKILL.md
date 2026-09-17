---
name: spec-driven-tdd-engineering
description: >-
  Use this skill when designing, building, fixing, or refactoring software features using GitHub Spec-Kit Spec-Driven Development (SDD) and Test-Driven Development (TDD). Enforces Human-in-the-Loop (HITL) gates at every stage: constitution alignment, spec approval, technical plan review, task authorization, failing test confirmation (Red), minimal code validation (Green/Refactor), and final merge sign-off.
---

# Spec-Driven TDD Engineering Skill

This skill guides agents through a defect-free engineering workflow combining **[GitHub Spec-Kit](https://github.com/github/spec-kit)** Spec-Driven Development (SDD) with **Test-Driven Development (TDD)**, enforced by mandatory **Human-in-the-Loop (HITL)** review gates.

---

## Agent Behavior Mandate: Mandatory Human Gates

> [!CAUTION]
> **AUTONOMOUS RUNAWAY IS STRICTLY FORBIDDEN.**
> You MUST stop and present your work at each `🚦 HUMAN GATE`. Do NOT execute subsequent stages or code modifications until the user provides explicit approval. If the user provides feedback or requests changes, incorporate them and re-present at the same gate.
>
> Detailed protocol & response handling: [references/human_in_the_loop_protocol.md](./references/human_in_the_loop_protocol.md)

---

## 4-Stage Spec-Kit + TDD Pipeline with 7 Human Gates

```text
[ 1. Constitution ] -> [ 2. Specify & Plan ] -> [ 3. TDD Tasks Loop ] -> [ 4. Verify & Sign-off ]
  🚦 Gate 1: Align       🚦 Gate 2: spec.md       Per Task:                🚦 Gate 7: Final Sign-off
                         🚦 Gate 3: plan.md       🚦 Gate 5: RED test
                         🚦 Gate 4: tasks.md      🚦 Gate 6: GREEN code
```

---

## Stage 1: Check & Enforce Project Constitution

Every feature must conform to the repository's foundational rules before work begins:

1. **Read Constitution**:
   - Inspect `.specify/constitution.md` for non-negotiable architectural, testing, and security principles.
   - Template: [templates/speckit_constitution_template.md](./templates/speckit_constitution_template.md)
2. **Spec-Kit Deep Dive Guide**:
   - For complete philosophy and command lifecycle: [references/github_spec_kit_guide.md](./references/github_spec_kit_guide.md)

> [!IMPORTANT]
> **🚦 HUMAN GATE 1: Constitution Alignment & Amendments**
> - **Present**: Summary of constitutional constraints relevant to the requested feature. Flag any architectural friction or ambiguity.
> - **Ask**: *"I have reviewed `.specify/constitution.md`. The constraints governing this work are: [summary]. Do these apply as written, or are any constitutional amendments or exceptions required?"*
> - **Action**: **STOP.** Wait for human approval before creating specifications.

---

## Stage 2: Spec-Driven Development (Specify & Plan)

Before touching production code or tests, construct and validate specifications:

### 2a. Scaffold Specification (`spec.md`)
1. Run: `python tools/speckit.py specify <feature-name>`
2. Define User Stories, In-Scope / Out-of-Scope boundaries, and Domain Invariants.
3. Template: [templates/speckit_specification_template.md](./templates/speckit_specification_template.md)
4. Methodology guide: [references/sdd_methodology.md](./references/sdd_methodology.md)

> [!IMPORTANT]
> **🚦 HUMAN GATE 2: Specification Approval**
> - **Present**: Executive summary of user stories, domain invariants, and out-of-scope boundaries. Link to [spec.md](./templates/speckit_specification_template.md).
> - **Ask**: *"Please review the specification draft. Are the domain invariants correct? Are there any missing acceptance criteria or edge cases? Do you approve this specification?"*
> - **Action**: **STOP.** Wait for human approval before authoring the technical blueprint.

### 2b. Draft Technical Blueprint (`plan.md`)
1. Run: `python tools/speckit.py plan <feature-name>`
2. Define component flow, file layout, public interface contracts, and error handling matrices.
3. Template: [templates/speckit_plan_template.md](./templates/speckit_plan_template.md)

> [!IMPORTANT]
> **🚦 HUMAN GATE 3: Technical Blueprint & Contract Approval**
> - **Present**: Component diagrams, public interface signatures, data schemas, and error matrix. Link to [plan.md](./templates/speckit_plan_template.md).
> - **Ask**: *"Please review the technical plan. Do the public interface signatures and data models meet your requirements? Is the error matrix complete? Do you approve this blueprint?"*
> - **Action**: **STOP.** Wait for human approval before generating tasks.

### 2c. Generate TDD Tasks (`tasks.md`)
1. Run: `python tools/speckit.py tasks <feature-name>`
2. Break requirements into sequential Red/Green/Refactor task items.
3. Template: [templates/speckit_tasks_template.md](./templates/speckit_tasks_template.md)

> [!IMPORTANT]
> **🚦 HUMAN GATE 4: Task Execution Authorization**
> - **Present**: Ordered breakdown of phases and individual TDD tasks. Link to [tasks.md](./templates/speckit_tasks_template.md).
> - **Ask**: *"Here is the TDD task breakdown. Is the task ordering and scope appropriate? Do you authorize beginning TDD execution on Phase 1?"*
> - **Action**: **STOP.** Wait for human authorization before writing test code.

---

## Stage 3: Test-Driven Development (TDD) Loop (Per Task)

Execute tasks sequentially in strict **Red -> Green -> Refactor** cycles with per-task gates:

### Step 1: RED (Write Failing Test)
1. Author test asserting the specific scenario from `spec.md` and contract from `plan.md`.
2. Avoid deep mocks; prefer in-memory fakes: [references/test_doubles_and_mocking.md](./references/test_doubles_and_mocking.md).
3. Run test runner and verify it fails with the expected assertion failure.

> [!IMPORTANT]
> **🚦 HUMAN GATE 5: Failing Test (Red) Approval**
> - **Present**: The failing test code snippet and runner output confirming the expected failure mode.
> - **Ask**: *"Task [X.Y] (RED): The test fails as expected with [assertion snippet]. Do you approve this test contract before I write the minimal implementation?"*
> - **Action**: **STOP.** Wait for human approval before writing implementation code.

### Step 2: GREEN (Minimal Implementation)
1. Author the minimal production code needed to satisfy the test assertions.
2. No speculative features or unasserted branches.

### Step 3: REFACTOR (Polish Under Test Protection)
1. Remove duplication, enforce strict typing, format code, and check linters.
2. Re-run test suite to guarantee zero regressions.
3. Lifecycle reference: [references/tdd_lifecycle.md](./references/tdd_lifecycle.md).

> [!IMPORTANT]
> **🚦 HUMAN GATE 6: Minimal Implementation & Refactor Approval**
> - **Present**: Implementation code diff/snippet, refactor summary, and runner output showing all tests passing.
> - **Ask**: *"Task [X.Y] (GREEN & REFACTOR): All tests pass cleanly. Refactor summary: [summary]. Do you approve this implementation to mark Task [X.Y] complete and move to the next task?"*
> - **Action**: **STOP.** Wait for human approval before proceeding to the next task.

*(Note: If the user explicitly commands fast-track mode, follow [references/human_in_the_loop_protocol.md](./references/human_in_the_loop_protocol.md) §6).*

---

## Stage 4: Invariant Verification & Checklist Audit

1. **Verify Invariants & Properties**:
   - Run property-based or boundary checks: [references/invariant_and_property_testing.md](./references/invariant_and_property_testing.md).
2. **Execute Quality Checklist**:
   - Fill out and audit: [templates/speckit_checklist_template.md](./templates/speckit_checklist_template.md).
3. **Verify Task Status**:
   ```bash
   python tools/speckit.py status
   ```

> [!IMPORTANT]
> **🚦 HUMAN GATE 7: Final Verification & Merge Sign-Off**
> - **Present**: Completed checklist summary, total test pass rate, code coverage, and clean lint/type status.
> - **Ask**: *"All tasks are complete, 100% of tests pass, and the Spec-Kit checklist is satisfied. Do you give final approval to merge / finalize this feature?"*
> - **Action**: **STOP.** Await final human authorization.

---

## Reference Guides & Templates

| Resource | Purpose |
| :--- | :--- |
| [references/human_in_the_loop_protocol.md](./references/human_in_the_loop_protocol.md) | **HITL philosophy, gate rules, responses, revisions & escalations** |
| [references/github_spec_kit_guide.md](./references/github_spec_kit_guide.md) | Spec-Kit artifact lifecycle and CLI usage |
| [references/sdd_methodology.md](./references/sdd_methodology.md) | Spec-Driven Development deep dive |
| [references/tdd_lifecycle.md](./references/tdd_lifecycle.md) | Red-Green-Refactor mechanics |
| [references/invariant_and_property_testing.md](./references/invariant_and_property_testing.md) | Invariant and property-based test designs |
| [references/test_doubles_and_mocking.md](./references/test_doubles_and_mocking.md) | Mocks vs. fakes vs. stubs guidance |
| [templates/speckit_constitution_template.md](./templates/speckit_constitution_template.md) | Repository constitution template |
| [templates/speckit_specification_template.md](./templates/speckit_specification_template.md) | Feature specification template with review gate |
| [templates/speckit_plan_template.md](./templates/speckit_plan_template.md) | Technical blueprint template with review gate |
| [templates/speckit_tasks_template.md](./templates/speckit_tasks_template.md) | TDD task list template with authorization gate |
| [templates/speckit_checklist_template.md](./templates/speckit_checklist_template.md) | Final quality audit checklist with sign-off gate |
| [examples/README.md](./examples/README.md) | Python & TypeScript reference implementations |
