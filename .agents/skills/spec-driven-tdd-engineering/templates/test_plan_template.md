# Test Plan & Execution Matrix Template

**Component**: [Target Module]  
**Spec Reference**: [Link to SDD Spec]  
**Test Runner**: [pytest / jest / vitest / go test]  

---

## 1. Test Suite Architecture

```text
tests/
├── unit/
│   └── test_[module].py       # Pure logic, fast, isolated
├── integration/
│   └── test_[module]_flow.py  # Inter-component, database/service integration
└── invariants/
    └── test_[module]_props.py # Boundary and invariant assertions
```

---

## 2. Test Execution Matrix

| Test ID | Category | Target Method | Red Phase (Failed As Expected?) | Green Phase (Minimal Pass) | Refactored & Verified |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T01 | Happy Path | `execute()` | [ ] Yes (AssertionError) | [ ] Yes | [ ] Yes |
| T02 | Boundary | `execute()` with 0 | [ ] Yes (AssertionError) | [ ] Yes | [ ] Yes |
| T03 | Error Case | `execute()` invalid | [ ] Yes (Raises ValueError) | [ ] Yes | [ ] Yes |
| T04 | Invariant | `check_invariants()` | [ ] Yes (AssertionError) | [ ] Yes | [ ] Yes |

---

## 3. Red Phase Checklist
Before writing implementation code:
- [ ] Test was executed and failed.
- [ ] Failure was caused by an assertion check or missing behavior, not an unhandled compilation/syntax/import crash.
- [ ] Test failure message is crystal clear.

---

## 4. Green Phase Checklist
- [ ] Simplest possible code written to pass tests.
- [ ] No speculative features or unrelated refactorings introduced in this step.
- [ ] All tests pass cleanly (100% green).
