# Repository Constitution: Spec-Driven & Test-Driven Engineering

**Repository**: `TDD+SDD Skill` (Multi-Agent Workspace)  
**Effective Date**: 2026-09-17  
**Version**: 2.0.0  
**Framework Standard**: [GitHub Spec-Kit](https://github.com/github/spec-kit) & SDE Core  

---

## Article I: The Spec-First Imperative (SDD)
1. **Zero "Vibe Coding"**: No production code, internal refactoring, or tests shall be written without an approved specification (`spec.md`) and technical plan (`plan.md`).
2. **Artifact Hierarchy**:
   - `spec.md`: Documents user stories, acceptance criteria, and domain invariants.
   - `plan.md`: Documents software architecture, component contracts, and error matrices.
   - `tasks.md`: Deconstructs the plan into actionable TDD tasks.
   - `risk.md`: Documents risk tier, factors, and required review gates.
   - `impact.md`: Documents expected vs. actual architectural blast radius.
   - `verification.md`: Documents evidence-backed execution results.
3. **Domain Invariants**: Every subsystem must declare invariants that cannot be violated under any circumstance.

---

## Article II: Test-Driven Development Covenants (TDD)
1. **Red Before Green**: An agent or engineer must construct failing tests and verify the failure mode before writing implementation code.
2. **Intent-Driven Red**: The failure mode must be an expected domain assertion error. Syntax, import, or build failures are classified as infrastructure failures, not valid Red.
3. **Minimal Implementations**: Production code must only satisfy the assertions in the failing tests. Speculative features and dead code are forbidden.
4. **Continuous Refactoring**: Code hygiene, typing, and deduplication must occur under the protection of passing test suites.

---

## Article III: Dual Multi-Agent Portability & Progressive Disclosure
1. All Agent Skills must maintain dual compatibility for **Google Antigravity (AGY)** and **Anthropic Claude (Claude Code)**.
2. `.agents/skills/` and `.claude/skills/` must remain synchronized using `tools/sde.py skill sync`.
3. Skills must adhere to **Progressive Disclosure**: Lean `SKILL.md` (< 500 lines) with detailed theory in `references/`.

---

## Article IV: Framework Profile & Architectural Precedent
1. Framework-specific behavior lives in `profiles/` (Flutter, Android, Node).
2. **The Golden Precedence Rule**: Agents must follow existing repository architectural conventions (state management, DI, folder layout) before introducing personal preference.

---

## Article V: Risk-Based Human-in-the-Loop (HITL) Mandate
1. **Zero Autonomous Runaway on High Risk**: Autonomous runaway on HIGH and CRITICAL tasks is strictly forbidden.
2. **Calibrated Gates**:
   - **`LOW` (Fast Track)**: Safe refactor, minor UI. Spec $\rightarrow$ Plan $\rightarrow$ TDD $\rightarrow$ Verify without blocking intermediate gates. Final Gate 7 sign-off only.
   - **`MEDIUM`**: Requires Gate 2 (Spec Approval) and Gate 7 (Final Sign-off).
   - **`HIGH`**: Requires Gate 2 (Spec), Gate 3 (Plan), and Gate 7 (Final Sign-off).
   - **`CRITICAL`**: Requires Gate 0 (Pre-Execution Authorization) before touching files.
3. **Iterative Feedback Loop**: When revisions are requested, the agent updates the artifact and re-presents at the same gate.

---

## Article VI: Evidence & Truth Protocol
1. **Absolute Truth in Reporting**: Never represent `NOT_RUN` as `PASS`. Never claim tests, device verification, or CI passed unless they were actually executed.
2. **Evidence Logging**: Raw test output and analysis logs must be recorded in `.specify/specs/<feature>/evidence/`.
3. **Change Impact Auditing**: Discrepancies between expected scope (`impact.md`) and actual git modifications trigger `WARNING: Unexpected Change` requiring human review before completion.
