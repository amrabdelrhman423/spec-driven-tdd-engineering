# Feature Specification: [Feature Name]

**Feature ID**: `feat-[id]`  
**Status**: [DRAFT | REVIEW | APPROVED]  
**Created**: [YYYY-MM-DD]  

---

## 1. Problem Statement & User Value
- **Context**: What problem does this solve for the user or system?
- **User Stories**:
  - *As a* [role]
  - *I want to* [perform action]
  - *So that* [business value]

---

## 2. In-Scope & Non-Goals

### In-Scope
- [ ] [Feature capability 1]
- [ ] [Feature capability 2]

### Out-of-Scope (Non-Goals)
- What is intentionally NOT being built in this phase?

---

## 3. Domain Invariants
Non-negotiable conditions that must ALWAYS hold true:
1. **Invariant 1**: [e.g., Output value is strictly positive]
2. **Invariant 2**: [e.g., Valid state transitions only]

---

## 4. Acceptance Criteria (Given - When - Then)

### Scenario 1: [Standard Success Path]
- **Given**: [Pre-existing state]
- **When**: [Action invoked]
- **Then**: [Expected state and return]

### Scenario 2: [Boundary / Edge Case]
- **Given**: [Boundary threshold, e.g., 0, empty list, max value]
- **When**: [Action invoked]
- **Then**: [Expected handled response]

### Scenario 3: [Invalid Input Handling]
- **Given**: [Malformed input]
- **When**: [Action invoked]
- **Then**: [Specific error raised without side-effects]

---

## 5. Human Review Gate (🚦 GATE 2)

- [ ] **Scope Alignment**: In-scope vs. non-goals boundaries validated by human.
- [ ] **Domain Invariants**: Invariants confirmed to reflect business integrity requirements.
- [ ] **Acceptance Criteria**: Given-When-Then scenarios validated as complete.
- [ ] **Open Questions Resolved**:
  - [ ] Q1: [Agent question regarding boundary condition or domain ambiguity]
  - [ ] Q2: [Agent question regarding out-of-scope or edge case behavior]

**Human Approval Sign-Off**:
- **Reviewer**: `[Human User / Architect]`
- **Status**: `[PENDING | APPROVED | REVISION_REQUESTED]`
- **Date**: `[YYYY-MM-DD]`

