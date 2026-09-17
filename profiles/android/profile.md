# Android SDK Framework Profile

The **Android SDK Profile** provides native Android commands and conventions for Kotlin/Java codebases built with Gradle.

---

## Commands

- **Analyze / Lint**: `./gradlew lint`
- **Format**: `./gradlew ktlintCheck`
- **Unit Tests**: `./gradlew testDebugUnitTest`
- **Connected Tests**: `./gradlew connectedAndroidTest` (requires connected device/emulator; marked N/A if absent)
- **Build**: `./gradlew assembleDebug`

---

## Conventions
- Architecture: MVVM / Clean Architecture.
- Dependency Injection: Hilt / Dagger.
