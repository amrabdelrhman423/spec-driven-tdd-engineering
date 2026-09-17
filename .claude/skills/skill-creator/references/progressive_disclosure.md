# Progressive Disclosure for Agent Skills

## 1. What is Progressive Disclosure?

LLMs have finite context windows and incur processing latency when inundated with massive documents.
**Progressive Disclosure** is the architectural pattern where information is loaded incrementally:

```text
Level 0: Skill Metadata (name + description)
         ~ 50 tokens injected into system prompt.
                 │
                 ▼ (Agent decides to activate skill)
Level 1: Main SKILL.md Instructions
         ~ 500-1500 tokens (high-level workflow + checklist).
                 │
                 ▼ (Agent hits specific complex sub-task)
Level 2: Deep References, Schemas, & Scripts
         Loaded on demand by reading specific linked files.
```

---

## 2. Rules for Structuring Skills

1. **The 500-Line Limit**:
   Keep `SKILL.md` under 500 lines. If a section contains extensive tables, API specifications, or background theory, move it into `references/<topic>.md`.

2. **Actionable First**:
   Start `SKILL.md` with an immediate workflow diagram or numbered step-by-step checklist. The agent should be able to execute the first step without reading the entire document.

3. **Relative File Linking**:
   Always link referenced documents with relative markdown links:
   - Good: `[guide](./references/guide.md)`
   - Avoid: Absolute system paths like `/Users/name/...` which break across machines and environments.
