# Project Constitution: Engineering Principles & Non-Negotiables

**Repository**: [Project Name]  
**Effective Date**: [Date]  
**Version**: 1.0.0  

---

## 1. Core Engineering Principles

### I. Spec-Driven Development (SDD) is Mandatory
No production code or tests shall be authored without an approved specification (`spec.md`) and technical plan (`plan.md`). "Vibe coding" and speculative implementations are strictly prohibited.

### II. Test-Driven Development (TDD) Discipline
- Every production feature or bug fix must follow the **Red-Green-Refactor** cycle.
- Developers and AI agents must witness a failing test verifying the expected failure mode before authoring code to pass it.
- Never mock domain logic or data models; prefer in-memory fakes and contract testing.

### III. System Invariant Preservation
Every component must identify and document its non-negotiable domain invariants. Invariants must be asserted in unit/property tests.

---

## 2. Architectural & Quality Standards

- **Static Typing**: All new code must be fully type-annotated (Python type hints, TypeScript strict mode, Go types).
- **Zero Regressions**: 100% test pass rate required before any task is marked complete.
- **Documentation**: All public APIs, CLI flags, and configuration schemas must include descriptive documentation.

---

## 3. Agent Execution Rules

1. Agents must check `.specify/constitution.md` before commencing any feature.
2. If requirements conflict with this constitution, the constitution takes precedence unless an explicit amendment is approved.
3. **Human-in-the-Loop Mandate**: Agents must stop and obtain human approval at all defined gates (constitution, spec, plan, tasks, red test, green implementation, final audit). Autonomous execution past gates without explicit approval is strictly prohibited.

