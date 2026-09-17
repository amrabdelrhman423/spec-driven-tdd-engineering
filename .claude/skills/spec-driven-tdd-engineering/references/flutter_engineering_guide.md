# Flutter Engineering & TDD Guide

A complete guide to applying Spec-Driven Development, TDD, and Risk-Based HITL inside Flutter projects.

---

## 1. Architectural Precedent Rules

1. **State Management**:
   - Inspect `pubspec.yaml`. If `flutter_bloc` is present, use Bloc/Cubit. If `flutter_riverpod` is present, use Riverpod. If `provider` is present, use Provider.
   - Do NOT introduce a second state management package if one is already established.
2. **Dependency Injection**:
   - Inspect for `get_it`. If present, register new dependencies in the existing locator registration function.
3. **Folder Layout**:
   - Follow existing layout: Feature-First (`lib/features/<name>/`) or Layer-First (`lib/presentation/`, `lib/domain/`, etc.).

---

## 2. Flutter TDD Lifecycle (Red -> Green -> Refactor)

### 1. The Red Phase
- Author unit test (e.g. `test/features/login/presentation/login_cubit_test.dart`).
- State the **Test Intent**:
  - *What behavior does this test prove?*
  - *Why should it fail before implementation?*
- Run `flutter test test/...` and verify an **AssertionError** (expected RED), not a syntax/import error.

### 2. The Green Phase
- Write minimal Cubit/UseCase/Widget logic to pass the test.
- Re-run `flutter test`. Verify exit code 0.

### 3. The Refactor Phase
- Format: `dart format .`
- Analyze: `flutter analyze`
- Clean up magic numbers and duplicate logic while keeping tests 100% passing.

---

## 3. Verification & Evidence
- Save `flutter test` output to `.specify/specs/<feature>/evidence/tests.txt`.
- Save `flutter analyze` output to `.specify/specs/<feature>/evidence/analysis.txt`.
- Record results in `verification.md`.
