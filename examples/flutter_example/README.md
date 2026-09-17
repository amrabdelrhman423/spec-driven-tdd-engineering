# Flutter Reference Example: User Authentication Feature

This example demonstrates how the **SDE Core**, **Flutter Profile**, **Risk-Based HITL**, and **Evidence System** operate in a real Flutter project.

---

## Architecture Implemented

- **Framework Profile**: `flutter`
- **State Management**: `flutter_bloc` (`Cubit` state machine)
- **Dependency Injection**: `get_it` service locator
- **Architecture**: Feature-First Clean Architecture (`lib/features/auth/`)
- **TDD Rigor**: Intent-driven unit tests verifying state streams and domain invariants (`test/features/auth/presentation/cubit/login_cubit_test.dart`)

---

## Artifacts Generated During the Workflow

1. **Specification**: [`specs/spec.md`](./specs/spec.md) (User stories, Given-When-Then criteria, domain invariants).
2. **Technical Blueprint**: [`specs/plan.md`](./specs/plan.md) (Mermaid diagrams, interfaces, error matrix).
3. **Risk Assessment**: [`specs/risk.md`](./specs/risk.md) (Assessed `MEDIUM` risk due to authentication credentials).
4. **Change Impact Scope**: [`specs/impact.md`](./specs/impact.md) (Expected files across Presentation, State, Domain, Data, DI).
5. **Implementation Tasks**: [`specs/tasks.md`](./specs/tasks.md) (Sequential Red-Green-Refactor cycles).
6. **Verification Report**: [`specs/verification.md`](./specs/verification.md) (Test execution results, evidence logs, N/A integration status).

---

## How to Test This Example

In any Flutter environment with Flutter 3.x installed:

```bash
cd .agents/skills/spec-driven-tdd-engineering/examples/flutter_example
flutter test
```
