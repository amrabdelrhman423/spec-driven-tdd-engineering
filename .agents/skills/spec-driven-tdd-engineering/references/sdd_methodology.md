# Spec-Driven Development (SDD) Methodology

## 1. Core Philosophy of SDD

Spec-Driven Development (SDD) is an engineering practice where formal specifications and architectural contracts are authored, reviewed, and finalized **before** writing tests or production code.

In autonomous and AI-assisted agent workflows, SDD serves as the anchor of truth. It eliminates hallucinations, scope creep, and untested edge cases by establishing clear boundaries up front.

```mermaid
flowchart LR
    A[User Goal / Requirements] --> B[Domain Analysis & Invariants]
    B --> C[Draft SDD Specification]
    C --> D[Review & Alignment Gate]
    D --> E[TDD Phase: Red Tests]
```

---

## 2. Key Elements of an SDD Specification

Every SDD Specification must define:

### A. Context & Purpose
- What user need or system capability does this address?
- What is explicitly **in-scope** and **out-of-scope**?

### B. Domain Model & Invariants
- Entities, value objects, and states.
- System Invariants: Rules that MUST hold true at all times (e.g., "Account balance can never be negative", "Every order item must have a positive quantity").

### C. Interface & Contract Definition
- Function signatures, parameter types, return types.
- Pre-conditions: What must be true before calling?
- Post-conditions: What is guaranteed after calling?
- Error Contract: Explicit list of error conditions and exceptions/codes raised.

### D. Behavioral Scenarios (Given - When - Then)
Structured acceptance criteria using BDD style:
- **Given** an existing cart with items totaling $100 and coupon 'SAVE10'
- **When** the discount calculator processes the cart
- **Then** a 10% discount ($10) is applied, resulting in a total of $90.

### E. Edge Cases & Boundary Matrix
A systematic matrix testing:
- Min / Max boundaries (0, 1, INT_MAX, empty collections)
- Malformed inputs (null, undefined, invalid formats)
- Concurrency or idempotency scenarios

---

## 3. The SDD Alignment Gate

Before writing tests or code:
1. Verify all ambiguous assumptions are resolved.
2. Confirm that public API contracts (names, types, signatures) match existing architecture.
3. Validate that the spec is testable (deterministic, observable side effects).
