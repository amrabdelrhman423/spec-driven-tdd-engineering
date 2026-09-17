# Flutter Testing & Verification Strategy

This document governs test construction, execution, and evidence collection for Flutter repositories under the SDE framework.

---

## 1. Testing Taxonomy

### 1. Unit Tests (`test/unit/` or `test/`)
- **Target**: Pure Dart logic, Value Objects, Domain Entities, UseCases, Repositories, DataSources, Bloc/Cubit states.
- **Tools**: `test`, `mocktail` or `mockito`, `bloc_test`.
- **Command**:
  ```bash
  flutter test test/path/to/unit_test.dart
  ```
- **Principle**: Fast, deterministic, memory-only execution. No Flutter UI binding required.

### 2. Widget Tests (`test/widgets/` or `test/`)
- **Target**: UI components, buttons, form inputs, dialogs, state-to-widget rendering.
- **Tools**: `flutter_test` (`WidgetTester`, `find`, `tester.pump()`, `tester.pumpAndSettle()`).
- **Command**:
  ```bash
  flutter test test/path/to/widget_test.dart
  ```
- **Principle**: Tests user interaction and visual state transitions without launching a real device emulator.

### 3. Integration Tests (`integration_test/`)
- **Target**: Complete cross-screen journeys, platform channels, native camera/location plugins, persistence.
- **Tools**: `integration_test` package (`IntegrationTestWidgetsFlutterBinding`).
- **Command**:
  ```bash
  flutter test integration_test/app_test.dart
  ```
- **Conditional Rule**:
  > **If `integration_test/` does not exist in the repository root, integration testing is classified as `N/A`.**
  > It must NEVER be marked as `PASS` unless the suite was actually executed against a running simulator, emulator, or real hardware.

### 4. Real-Device Verification
- **Target**: Verifying release behavior, hardware accelerations, push notifications, and native performance.
- **Evidence Fields**:
  - `Device`: e.g. "Google Pixel 7" or "iPhone 14 Pro"
  - `OS`: e.g. "Android 13" or "iOS 16.5"
  - `Scenario`: User flow description
  - `Expected`: Exact expected UI response
  - `Actual`: Verified outcome with screenshot/recording
- **Conditional Rule**:
  > **If real device verification was not performed, mark status as `N/A` or `NOT_RUN`.**

---

## 2. Command Execution Sequence

```bash
# 1. Static Analysis
flutter analyze

# 2. Formatting Check
dart format --output=none --set-exit-if-changed .

# 3. Unit and Widget Test Suite
flutter test

# 4. Integration Test Suite (Conditional)
# Only run if directory exists
test -d integration_test && flutter test integration_test

# 5. Production Build Validation (Release Smoke Check)
flutter build apk --debug
```

All execution outputs must be piped to `.specify/specs/<feature>/evidence/` and summarized in `verification.md`.
