# Verification Report: [Feature Name]

## Summary Status
- **Specification Compliance**: `[PASS | FAIL]`
- **Overall Suite Pass**: `[PASS | INCOMPLETE / FAIL]`

---

## 1. Specification & Acceptance Criteria
**Status**: `[PASS | FAIL]`  
All Given-When-Then scenarios verified against implementation.

---

## 2. Automated Tests (Unit & Widget)
**Status**: `[PASS | FAIL | NOT_RUN]`  
**Command**: `[e.g. flutter test / npm test / python -m unittest]`  
**Result**: `[Pass count, duration, assertions satisfied]`  
**Evidence Log**: [`tests.txt`](./evidence/tests.txt)

---

## 3. Static Analysis & Lint
**Status**: `[PASS | FAIL | NOT_RUN]`  
**Command**: `[e.g. flutter analyze / dart format]`  
**Result**: `[Zero issues found]`  
**Evidence Log**: [`analysis.txt`](./evidence/analysis.txt)

---

## 4. Build Verification
**Status**: `[PASS | FAIL | NOT_RUN | N/A]`  
**Command**: `[e.g. flutter build apk / npm run build]`  
**Result**: `[Build exit code and artifact output]`  
**Evidence Log**: [`build.txt`](./evidence/build.txt)

---

## 5. Integration Tests
**Status**: `[PASS | FAIL | NOT_RUN | N/A]`  
**Command**: `[e.g. flutter test integration_test]`  
**Result**: `[N/A if directory does not exist; or pass result if executed]`  
**Evidence Log**: [`integration.txt`](./evidence/integration.txt)

---

## 6. Real Device Verification
**Status**: `[PASS | FAIL | NOT_RUN | N/A]`  
- **Device**: `[e.g. Google Pixel 7 / iPhone 14 Pro]`
- **OS**: `[e.g. Android 14 / iOS 17]`
- **Scenario**: `[Detailed physical interaction tested]`
- **Expected**: `[Expected UI rendering or behavior]`
- **Actual**: `[Actual observed behavior]`

---

## 7. CI Pipeline Status
**Status**: `[PASS | FAIL | NOT_RUN]`  
Workflow run link or local runner pass.

---

## 8. Deployment Status
**Status**: `[PASS | FAIL | NOT_RUN | N/A]`  

---

## 9. Captured Evidence Artifacts
- [`tests.txt`](./evidence/tests.txt)
- [`analysis.txt`](./evidence/analysis.txt)
- [`build.txt`](./evidence/build.txt)
- [`integration.txt`](./evidence/integration.txt)

---

## 10. Remaining Risks
- [ ] [Any residual known trade-offs or technical debt]
