# Framework Profiles Guide

Framework Profiles decouple the **core SDE workflow** from platform-specific command lines, test frameworks, and project directory structures.

---

## 1. Supported Profiles

| Profile | Platform | Primary Language | Flagship Tools |
| :--- | :--- | :--- | :--- |
| **`flutter`** | Mobile, Desktop, Web | Dart | `flutter test`, `flutter analyze`, `dart format`, `flutter build apk` |
| **`android`** | Mobile | Kotlin / Java | Gradle (`./gradlew testDebugUnitTest`, `./gradlew lint`) |
| **`node`** | Backend, Fullstack | JS / TypeScript | `npm test`, `node --test`, `npm run lint` |
| **`generic`** | Agnostic | Multi | Standard CLI runners |

---

## 2. Dynamic Command Resolution

A profile does not run commands blindly:
- If a command requires a directory that does not exist (e.g. `integration_test/`), the command is marked **`N/A`** and skipped.
- The test status in `verification.md` is recorded as **`N/A`**, preserving the integrity of test evidence.

---

## 3. Creating New Profiles

To add a new framework profile (e.g. `go`, `rust`, `python`):
1. Create `profiles/<name>/commands.yaml`.
2. Document conventions and testing in `profiles/<name>/profile.md`.
3. Register the detection marker in `core/profiles.py`.
