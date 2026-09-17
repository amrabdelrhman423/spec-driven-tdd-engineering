# TDD + SDD Verification Checklist

Use this checklist before marking any feature, bug fix, or refactoring task as complete.

---

## 1. Specification (SDD) Compliance
- [ ] Every requirement in the SDD specification has at least one corresponding test.
- [ ] No un-specified behaviors, hidden side-effects, or unauthorized public APIs were introduced.
- [ ] Domain invariants are explicitly stated and verified in the test suite.

---

## 2. Test Quality & Coverage
- [ ] Every test was proven to fail (Red) before the code was written.
- [ ] Tests test public behavior and state outcomes, not internal private implementation details.
- [ ] Edge cases tested:
  - [ ] Null / undefined / None inputs
  - [ ] Empty collections (empty lists, strings, dictionaries)
  - [ ] Boundary thresholds (0, negative numbers, maximum values)
  - [ ] Duplicate or idempotent calls
- [ ] No flaky tests (no unseeded randomness, no unmocked non-deterministic clocks or external network calls).

---

## 3. Code Cleanliness & Static Analysis (Refactor Phase)
- [ ] Code is free of duplication (DRY).
- [ ] Variable and function names are intention-revealing.
- [ ] Static type checks pass without warnings (`mypy`, `tsc`, etc.).
- [ ] Linter passes without warnings or suppressions.
- [ ] All tests remain green after refactoring.
