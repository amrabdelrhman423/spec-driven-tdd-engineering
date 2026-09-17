# Evidence-Driven Verification Protocol

In the SDE framework, **no assertion of correctness is accepted without tangible, reproducible evidence**.

---

## 1. The Cardinal Truth Rules

> **Never represent `NOT_RUN` as `PASS`.**  
> **Never claim a test passed unless the test runner executed and returned exit code 0.**  
> **Never claim device verification unless the physical hardware interaction actually occurred.**  
> **Never claim CI passed unless the remote or local CI workflow ran cleanly.**

---

## 2. Standardized Status Taxonomy

Every verification item in `verification.md` must carry one of five explicit statuses:

| Status | Meaning | Acceptable Condition |
| :--- | :--- | :--- |
| **`PASS`** | Executed and succeeded | Exit code 0, all assertions verified. |
| **`FAIL`** | Executed and failed | Exit code non-zero, assertion or build error. |
| **`NOT_RUN`** | Planned but not yet executed | Check has not been triggered. |
| **`BLOCKED`** | Cannot execute due to external issue | Missing credentials, emulator offline, network outage. |
| **`N/A`** | Not applicable to this repository | e.g. `integration_test/` directory is absent. |

---

## 3. Evidence Artifacts Directory

All raw outputs are saved in `.specify/specs/<feature>/evidence/`:
- **`tests.txt`**: Complete stdout/stderr from test runner.
- **`analysis.txt`**: Linter and static analysis output.
- **`build.txt`**: Compiler and packaging output.
- **`integration.txt`**: Integration or E2E runner logs.
- **`screenshots/`**: Visual evidence of UI widget or physical device states.
