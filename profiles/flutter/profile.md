# Flutter Framework Profile

The **Flutter Framework Profile** equips the SDE system with specialized engineering knowledge for modern Flutter and Dart applications across iOS, Android, Web, and Desktop.

---

## 1. Capabilities & Scope

- **Language & SDK**: Dart 3.x, Flutter 3.x.
- **Verification Commands**:
  - Analysis: `flutter analyze`
  - Formatting: `dart format --output=none --set-exit-if-changed .`
  - Unit & Widget Tests: `flutter test`
  - Integration Tests: `flutter test integration_test` (conditional)
  - Production Builds: `flutter build apk`, `flutter build appbundle`, `flutter build ipa`
- **Testing Pyramid**:
  - **Unit Tests**: Domain logic, UseCases, Repositories, DataSources, Bloc/Cubit state machines.
  - **Widget Tests**: Component rendering, gestures, form validation, theme switching.
  - **Integration Tests**: End-to-end user flows, native platform plugins, SQLite/Hive storage.
  - **Real-Device Verification**: Physical device validation report.

---

## 2. Dynamic Command Resolution

The profile inspects the project tree before selecting commands:
- If `integration_test/` does not exist:
  - `integration_test` status = **`N/A`** (never reported as `PASS`).
- If `test/` contains only unit tests:
  - Widget test items are marked appropriately.
- If dependencies require code generation (`build_runner`):
  - Agent validates whether generated files (`*.g.dart`, `*.freezed.dart`) are up to date.

---

## 3. Reference Guides
- [Testing Strategy](./testing.md)
- [Conventions & Architecture Inspection](./conventions.md)
- [Command Manifest](./commands.yaml)
