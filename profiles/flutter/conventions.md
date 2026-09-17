# Flutter Architectural Precedent & Conventions Guide

In production engineering, code consistency is paramount. AI agents must **never impose personal preferences** or rewrite existing architectural patterns.

---

## The Golden Rule of Architecture Selection

> **Follow repository precedent before introducing personal preference.**

Before authoring a single line of Flutter or Dart code, inspect the codebase and follow this decision tree:

---

## 1. State Management Inspection

Inspect `pubspec.yaml` and existing files in `lib/`:

| Detected Pattern | Dependency Marker | Action |
| :--- | :--- | :--- |
| **Bloc / Cubit** | `flutter_bloc:`, `bloc:` | Create states extending `Equatable` or using `freezed`. Emit states via Cubit/Bloc. Use `BlocProvider`, `BlocBuilder`, `BlocListener`. |
| **Riverpod** | `flutter_riverpod:`, `riverpod:` | Use `StateNotifierProvider`, `NotifierProvider`, or `AsyncNotifier`. Access via `ConsumerWidget` or `ref.watch`. |
| **Provider** | `provider:` | Use `ChangeNotifier` with `notifyListeners()`. Consume via `Consumer` or `context.watch<T>()`. |
| **GetX** | `get:` | Use `GetxController` with `Rx` types or `update()`. Follow repository GetX patterns. |
| **Vanilla / setState** | No state management package | Use `StatefulWidget` or `ValueNotifier` without adding heavy third-party state frameworks unless authorized. |

---

## 2. Dependency Injection & Service Locator Inspection

| Detected Pattern | Dependency Marker | Action |
| :--- | :--- | :--- |
| **GetIt** | `get_it:` | Register dependencies via `getIt.registerLazySingleton<T>()` or `getIt.registerFactory<T>()` in an injection locator file (`injection.dart` or `locator.dart`). |
| **Injectable** | `injectable:` | Annotate classes with `@lazySingleton` or `@injectable`. Run `dart run build_runner build` after modifications. |
| **Riverpod DI** | `riverpod:` | Use provider dependency graphs (`Provider((ref) => ...)`) rather than external service locators. |
| **Constructor Injection** | No DI package | Pass dependencies explicitly through class constructors. |

---

## 3. Structural & Layering Conventions

Inspect folder structure inside `lib/`:

### Pattern A: Feature-First Clean Architecture
```text
lib/
├── core/
│   ├── errors/
│   ├── network/
│   └── utils/
└── features/
    └── [feature_name]/
        ├── data/
        │   ├── datasources/
        │   ├── models/
        │   └── repositories/
        ├── domain/
        │   ├── entities/
        │   ├── repositories/
        │   └── usecases/
        └── presentation/
            ├── cubit/ (or bloc/)
            ├── screens/ (or pages/)
            └── widgets/
```
*Rule: If this layout exists, place all new feature files within `lib/features/<new_feature>/` strictly adhering to the 3-tier layering.*

### Pattern B: Layer-First Clean Architecture
```text
lib/
├── presentation/
├── domain/
└── data/
```
*Rule: Group files by functional layer across the entire project.*

---

## 4. Code Generation Integrity (`build_runner`)

If the repository uses `freezed`, `json_serializable`, or `injectable`:
1. Always check if generated files (`*.freezed.dart`, `*.g.dart`) exist.
2. If modified, regenerate via:
   ```bash
   dart run build_runner build --delete-conflicting-outputs
   ```
3. Verify that `flutter analyze` passes with zero unresolved generation errors.
