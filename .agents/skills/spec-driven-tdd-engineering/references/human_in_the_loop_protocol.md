# Human-in-the-Loop (HITL) Protocol

This document establishes the official Human-in-the-Loop engineering protocol for the `spec-driven-tdd-engineering` skill. It governs how AI agents interact with humans across every stage of Spec-Driven Development (SDD) and Test-Driven Development (TDD).

---

## 1. Core Philosophy: Trust, Verify & Collaborate

In an autonomous or semi-autonomous development environment, agentic models excel at synthesizing code, generating test cases, and exploring edge conditions. However:
- Agents lack real-world business context and organizational history.
- Unchecked autonomy can lead to hallucinated requirements, speculative architecture ("vibe coding"), and silent regressions.
- **Human-in-the-Loop is not a bottleneck—it is a defect-prevention firewall.**

### The Prime Directive
> **An agent must NEVER transition between SDD phases or execute code modifications without presenting its work and obtaining explicit human approval at each designated gate.**

---

## 2. The 7 Engineering Gates

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

## 3. Detailed Gate Specifications

### Gate 1: Constitution Alignment Gate
- **Trigger**: Prior to scaffolding or designing any feature.
- **Agent Action**: Read `.specify/constitution.md`. Check for project-specific constraints (architectural patterns, security requirements, forbidden libraries).
- **Presentation to Human**:
  - Summarize the key constitutional rules that govern this feature.
  - Flag any potential friction or ambiguity between the requested feature and the constitution.
- **Mandatory Agent Prompt**:
  > *"I have reviewed `.specify/constitution.md`. The relevant constraints are [summary]. Do these constraints apply to this feature, or are any constitutional amendments or exceptions required before proceeding?"*
- **Wait Condition**: STOP and await human response.

### Gate 2: Specification Approval Gate (`spec.md`)
- **Trigger**: Immediately after drafting or modifying `.specify/specs/<feature>/spec.md`.
- **Agent Action**: Generate user stories, in-scope/out-of-scope boundaries, domain invariants, and Given-When-Then scenarios.
- **Presentation to Human**:
  - Provide a concise executive summary of the spec.
  - Highlight defined domain invariants and out-of-scope boundaries.
  - Link directly to the draft: `[spec.md](file:///path/to/spec.md)`.
- **Mandatory Agent Prompt**:
  > *"Here is the feature specification for `[feature-name]`. Please review the scope and domain invariants:*
  > *1. Are there any missing acceptance criteria or edge cases?*
  > *2. Are the out-of-scope boundaries acceptable?*
  > *Do you approve this specification to proceed to technical planning?"*
- **Wait Condition**: STOP and await human response.

### Gate 3: Technical Blueprint & Contract Approval Gate (`plan.md`)
- **Trigger**: Immediately after drafting `.specify/specs/<feature>/plan.md`.
- **Agent Action**: Design component diagrams, module/file layout, public interface contracts, and error matrices.
- **Presentation to Human**:
  - Present the proposed interfaces and data schemas.
  - Present the error handling and edge case matrix.
  - Link directly to the plan: `[plan.md](file:///path/to/plan.md)`.
- **Mandatory Agent Prompt**:
  > *"Here is the technical blueprint for `[feature-name]`. Please review the architecture and contracts:*
  > *1. Do the public interface signatures and data models meet your requirements?*
  > *2. Are the failure modes and error matrix comprehensive?*
  > *Do you approve this plan to proceed to task generation?"*
- **Wait Condition**: STOP and await human response.

### Gate 4: Task Execution Authorization Gate (`tasks.md`)
- **Trigger**: Immediately after generating `.specify/specs/<feature>/tasks.md`.
- **Agent Action**: Break down the plan into ordered, atomic Red-Green-Refactor tasks.
- **Presentation to Human**:
  - List the proposed implementation phases and task sequence.
  - Note any dependencies or ordering constraints.
  - Link directly to tasks: `[tasks.md](file:///path/to/tasks.md)`.
- **Mandatory Agent Prompt**:
  > *"Here is the implementation task list for `[feature-name]`. It contains [N] tasks structured in Red-Green-Refactor cycles:*
  > *1. Is the task breakdown and execution order appropriate?*
  > *2. Are there any tasks that should be added, reordered, or removed?*
  > *Do you authorize starting TDD execution on Phase 1?"*
- **Wait Condition**: STOP and await human response.

### Gate 5: Failing Test (Red) Approval Gate (Per-Task)
- **Trigger**: After writing the failing test for an individual task item and running it.
- **Agent Action**:
  - Write test code strictly targeting the spec scenario.
  - Execute test runner (`pytest`, `unittest`, `node --test`, `npm test`).
  - Capture and verify the test failure output.
- **Presentation to Human**:
  - Show the test code snippet.
  - Show the test runner failure output demonstrating the expected assertion failure (not a syntax error or import crash).
- **Mandatory Agent Prompt**:
  > *"Task [X.Y] (RED): I have written the failing test for `[scenario]`. The test fails as expected with:*
  > `[AssertionError snippet]`
  > *Do you approve this test contract before I write the minimal implementation?"*
- **Wait Condition**: STOP and await human response.

### Gate 6: Minimal Code & Refactor (Green) Approval Gate (Per-Task)
- **Trigger**: After implementing minimal production code to pass the test and refactoring.
- **Agent Action**:
  - Write minimal code to pass tests.
  - Refactor for cleanliness, typing, and readability.
  - Execute full test suite and confirm all tests pass cleanly.
- **Presentation to Human**:
  - Show the implemented production code diff or snippet.
  - Show the test runner output confirming all tests pass.
  - Note any refactorings applied.
- **Mandatory Agent Prompt**:
  > *"Task [X.Y] (GREEN & REFACTOR): The implementation passes all tests cleanly ([M] tests passed in [S]s). Cleanups applied: [summary].*
  > *Do you approve this implementation to mark Task [X.Y] complete and proceed to Task [X.Z]?"*
- **Wait Condition**: STOP and await human response.

### Gate 7: Final Verification & Merge Sign-Off Gate
- **Trigger**: After all tasks are completed and static analysis/checklists are executed.
- **Agent Action**:
  - Run full test suite across the entire repository.
  - Run linters, formatters, and type checkers (`mypy`, `tsc`).
  - Complete `.specify/specs/<feature>/checklist.md`.
- **Presentation to Human**:
  - Present the completed checklist summary.
  - Present aggregate test results and code coverage metrics.
  - Link directly to the completed checklist: `[checklist.md](file:///path/to/checklist.md)`.
- **Mandatory Agent Prompt**:
  > *"All [N] tasks for `[feature-name]` are complete. All test suites pass (100%), types check cleanly, and the Spec-Kit checklist is satisfied.*
  > *Here is the final checklist summary. Do you give final approval to merge / finalize this feature?"*
- **Wait Condition**: STOP and await human response.

---

## 4. Human Feedback & Revision Protocol

When the human responds at any gate, the agent must categorize the response:

### 1. Approval Responses
- **Examples**: `"approved"`, `"proceed"`, `"yes"`, `"looks good"`, `"lgtm"`, `"continue"`, `"next"`, `"go ahead"`, `"ship it"`.
- **Action**: Check off the gate in the relevant markdown document, log approval, and advance immediately to the next stage.

### 2. Revision & Correction Requests
- **Examples**: `"Change the return type to an enum"`, `"Add an edge case for negative balances"`, `"Rename this method"`.
- **Action**:
  1. Acknowledge the requested changes.
  2. Apply the modifications to the artifact (spec, plan, test, or code).
  3. Re-run any relevant validations or tests.
  4. **Re-present the revised artifact at the SAME gate**:
     > *"I have updated [artifact] according to your feedback: [summary of changes]. Do you approve this revised version to proceed?"*
  5. Repeat until explicit approval is granted.

### 3. Ambiguity or Clarification Inquiries
- **Examples**: `"Why did you choose an in-memory repository?"`, `"What happens if the network times out?"`.
- **Action**:
  1. Provide a concise, clear technical explanation.
  2. Offer concrete alternatives if relevant.
  3. Re-ask the approval question.

---

## 5. Escalation Rules: When to Stop Immediately

The agent must stop immediately and ask for guidance whenever:
1. **Architectural Contradiction**: A requested feature directly conflicts with an article in `.specify/constitution.md`.
2. **Breaking API Change**: Implementation would break existing public interfaces, APIs, or downstream test suites.
3. **Ambiguous Business Logic**: Multiple valid interpretations exist for a domain rule, and guessing could cause data corruption or security flaws.
4. **Third-Party Dependency Addition**: A proposed solution requires adding a new external library or package not already in the repository's dependency manifest.

---

## 6. Fast-Track Mode (Explicit Human Authorization Only)

By default, every single task in Stage 3 requires Gates 5 and 6.

If the human user explicitly instructs the agent to fast-track:
- **Example user prompts**: `"Auto-run Phase 2"`, `"Skip per-task approval"`, `"Fast-track tasks 2.1 through 2.5"`.
- **Permitted Agent Behavior**:
  1. The agent may execute the specified TDD tasks autonomously (still following Red -> Green -> Refactor strictly).
  2. The agent must pause and notify immediately if any test fails unexpectedly or cannot be made green within 2 attempts.
  3. **Gate 7 (Final Sign-Off) is NEVER skippable.** The agent must always present the final results and checklist for human approval before completing the feature.
