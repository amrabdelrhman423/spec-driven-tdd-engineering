# Repository Constitution: Spec-Driven & Test-Driven Engineering

**Repository**: `TDD+SDD Skill` (Multi-Agent Workspace)  
**Effective Date**: 2026-09-17  
**Version**: 1.0.0  
**Framework Standard**: [GitHub Spec-Kit](https://github.com/github/spec-kit)  

---

## Article I: The Spec-First Imperative (SDD)
1. **Zero "Vibe Coding"**: No production code, internal refactoring, or tests shall be written without an approved specification (`spec.md`) and technical plan (`plan.md`).
2. **Artifact Hierarchy**:
   - `spec.md`: Documents user stories, acceptance criteria, and domain invariants.
   - `plan.md`: Documents software architecture, component contracts, and error matrices.
   - `tasks.md`: Deconstructs the plan into actionable TDD tasks.
3. **Domain Invariants**: Every subsystem must declare invariants that cannot be violated under any circumstance.

---

## Article II: Test-Driven Development Covenants (TDD)
1. **Red Before Green**: An agent or engineer must construct failing tests and verify the failure mode before writing implementation code.
2. **Minimal Implementations**: Production code must only satisfy the assertions in the failing tests. Speculative features and dead code are forbidden.
3. **Continuous Refactoring**: Code hygiene, typing, and deduplication must occur under the protection of passing test suites.

---

## Article III: Dual Multi-Agent Portability
1. All Agent Skills must maintain dual compatibility for **Google Antigravity (AGY)** and **Anthropic Claude (Claude Code)**.
2. `.agents/skills/` and `.claude/skills/` must remain synchronized using `tools/skill_builder.py sync`.
3. Skills must adhere to **Progressive Disclosure**: Lean `SKILL.md` (< 500 lines) with detailed theory in `references/`.

---

## Article IV: Quality Gates & Verification
1. All unit and integration test suites must pass 100% cleanly without warnings.
2. Link integrity across all markdown documentation and specifications must be strictly verified.

---

## Article V: Human-in-the-Loop (HITL) Mandate
1. **Zero Autonomous Runaway**: The agent must NEVER autonomously execute the full SDD+TDD pipeline without stopping at each defined gate for human review and explicit approval.
2. **Mandatory Checkpoints**: Every specification (`spec.md`), architectural blueprint (`plan.md`), task plan (`tasks.md`), failing test (Red phase), implementation (Green phase), and final checklist audit must be presented to the human.
3. **Specific Inquiry**: At each gate, the agent must ask specific, targeted questions addressing domain invariants, boundaries, interfaces, or trade-offs rather than generic "is this okay?" prompts.
4. **Iterative Feedback Loop**: When a human reviewer requests revisions or answers clarification questions, the agent must apply the changes and re-present at the same gate until explicit authorization is granted.

