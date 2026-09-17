# Risk Assessment & Classification Guide

The SDE Risk Model classifies development tasks into four tiers: **LOW**, **MEDIUM**, **HIGH**, and **CRITICAL**. This enables dynamic Human-in-the-Loop oversight—granting speed to safe, local changes while enforcing rigorous verification and multi-signature gates on high-consequence operations.

---

## 1. The Four Risk Tiers

```text
┌──────────────┬──────────────────────────────────────────┬────────────────────────────────────────────┐
│ Tier         │ Typical Changes                          │ Human Gate Lifecycle                       │
├──────────────┼──────────────────────────────────────────┼────────────────────────────────────────────┤
│ **LOW**      │ Small UI tweaks, text, formatting, safe  │ **Fast Track**: Spec → Plan → TDD → Verify │
│              │ refactoring, single-widget styling.      │ (Final Gate 7 verification only)           │
├──────────────┼──────────────────────────────────────────┼────────────────────────────────────────────┤
│ **MEDIUM**   │ Standard features, state management, API │ Spec Approval (Gate 2) → Plan → TDD →      │
│              │ consumption, DB queries, local auth.     │ Verify & Sign-Off (Gate 7)                 │
├──────────────┼──────────────────────────────────────────┼────────────────────────────────────────────┤
│ **HIGH**     │ Payments, security, PII, architectural   │ Spec (Gate 2) → Plan (Gate 3) → TDD →      │
│              │ redesign, breaking interface changes.    │ Verify & Sign-Off (Gate 7)                 │
├──────────────┼──────────────────────────────────────────┼────────────────────────────────────────────┤
│ **CRITICAL** │ Production DB deletion, credential/key   │ **Gate 0 Pre-Execution Authorization**     │
│              │ modification, destructive migration.     │ + Gates 2, 3, 4, 7 (Strict Sign-off)       │
└──────────────┴──────────────────────────────────────────┴────────────────────────────────────────────┘
```

---

## 2. Risk Factors Checklist

Every non-trivial feature must evaluate these six core dimensions:

1. **Architecture Change**: Does this introduce a new pattern, layer, or subsystem?
2. **Security Sensitive / PII**: Does this touch passwords, tokens, encryption, or user private data?
3. **Data Migration**: Does this alter database schema, file storage formats, or serialized state?
4. **Production Impact**: Can a failure immediately impair live users or external services?
5. **Breaking Contract**: Does this alter public interface signatures, CLI flags, or API schemas?
6. **Irreversible Deletion**: Can this permanently destroy production data or configurations?

---

## 3. Fast-Track Mode (LOW Risk)

For cosmetic or localized changes:
- Do NOT block the developer with multiple intermediate approval questions.
- Maintain full SDD & TDD discipline (write failing test, minimal passing code, capture evidence).
- Stop only at Gate 7 with the verified diff and evidence log.
