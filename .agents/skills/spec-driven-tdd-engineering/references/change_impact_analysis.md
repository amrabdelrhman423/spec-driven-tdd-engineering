# Change Impact Analysis Guide

Change Impact Analysis guards against **unintended modifications, creeping side effects, and architectural decay**.

---

## 1. Pre-Implementation Estimation

Before editing source files, the agent defines the **Expected Architectural Scope** across standard application layers:
- **Presentation**: UI widgets, screens, pages.
- **State**: Bloc, Cubit, Riverpod Notifiers, ViewModels.
- **Domain**: Entities, UseCases, Repository interfaces.
- **Data**: DataSources, DTOs, API clients, local persistence models.
- **Dependency Injection**: Registration files (`injection.dart`, service locators).
- **Tests**: Corresponding test suites.
- **Config**: Manifests, `pubspec.yaml`, `package.json`.

This scope is persisted to `.specify/specs/<feature>/impact.md`.

---

## 2. Post-Implementation Audit

Upon completing the Green & Refactor phase:
1. Run:
   ```bash
   python tools/sde.py feature impact <feature> --audit
   ```
2. The analyzer compares the Git diff against the expected scope.
3. If unexpected files are touched:
   - **Trigger**: `WARNING: Unexpected Change`
   - **Requirement**: The agent must explain the rationale for modifying unpredicted files. No automatic revert occurs; the developer reviews the architectural rationale before proceeding to verification.
