# Framework Profiles

Framework Profiles decouple the **framework-agnostic SDE Core** from language- and platform-specific commands, conventions, test types, and build scripts.

---

## Profile Architecture

Each profile defines:
1. **`profile.md`**: Architectural philosophy, supported platforms, and progressive disclosure guidelines.
2. **`commands.yaml`**: Command definitions for static analysis, formatting, unit/widget/integration testing, and production builds.
3. **`testing.md`**: Testing taxonomy (unit, widget, integration, golden, real-device verification) and command resolution rules.
4. **`conventions.md`**: Architectural precedent inspection (state management, dependency injection, folder layout).

```text
profiles/
├── README.md
├── flutter/             # First-class production profile
│   ├── profile.md
│   ├── commands.yaml
│   ├── testing.md
│   └── conventions.md
├── android/             # Lightweight Android SDK profile
│   ├── profile.md
│   └── commands.yaml
└── node/                # Lightweight Node.js profile
    ├── profile.md
    └── commands.yaml
```

---

## Profile Discovery & Precedence Rule

When an agent or developer operates inside a workspace:
1. **Auto-Detection**: The SDE profile engine inspects repository markers (`pubspec.yaml`, `build.gradle`, `package.json`).
2. **The Golden Precedence Rule**:
   > **Always follow repository precedent before introducing personal preference.**
   > If the target repository uses Bloc, do not introduce Riverpod. If it uses GetIt, do not introduce Provider. If it follows Feature-First, do not introduce Layer-First.
3. **Conditional Command Resolution**:
   > If an optional directory (such as `integration_test/`) is absent, mark the status as **`N/A`**, never **`PASS`**.
