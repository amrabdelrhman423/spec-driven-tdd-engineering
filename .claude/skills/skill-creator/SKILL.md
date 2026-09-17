---
name: skill-creator
description: >-
  Use this skill when authoring, scaffolding, designing, linting, or validating new Agent Skills compatible with Google Antigravity (AGY) and Anthropic Claude. Enforces YAML frontmatter schema, progressive disclosure directory structure, and link integrity.
---

# Agent Skill Creator & Scaffolder

This meta-skill provides standard workflows for creating, structuring, and maintaining portable **Agent Skills** that work across both **Google Antigravity (AGY)** and **Anthropic Claude (Claude Code)**.

---

## 4-Step Skill Authoring Lifecycle

```text
[ 1. Scaffold ]        -> [ 2. Author ]            -> [ 3. Validate ]     -> [ 4. Sync ]
python skill_builder.py    Write SKILL.md &           python skill_builder.py    python skill_builder.py
new <name>                 references/                validate <name>            sync
```

---

## Step 1: Scaffold a New Skill

Run the scaffolding CLI command from the repository root:

```bash
python tools/skill_builder.py new <skill-name> --desc "Use this skill when..."
```

This automatically creates the standard structure:
```text
.agents/skills/<skill-name>/
├── SKILL.md                  # Main entry point with frontmatter
├── references/               # Bulky documentation loaded on demand
│   └── guide.md
├── templates/                # Reusable document templates
│   └── template.md
├── scripts/                  # Shell or Python automation scripts
└── examples/                 # Working reference examples
    └── README.md
```

---

## Step 2: Authoring with Progressive Disclosure

1. **Frontmatter Configuration**:
   - `name`: Must match the directory name (lowercase, alphanumeric, hyphenated).
   - `description`: The single most critical field. Always use third person and specify the exact trigger conditions:
     ```yaml
     ---
     name: database-migrator
     description: >-
       Use this skill when creating, verifying, or rolling back PostgreSQL database
       migrations, modifying database schemas, or debugging SQL migration failures.
     ---
     ```
2. **Keep `SKILL.md` Concise (< 500 lines)**:
   - Provide a high-level numbered workflow and immediately actionable checklist.
   - Offload extensive reference tables, API schemas, and theoretical guides to `references/`.
   - Learn more: [references/progressive_disclosure.md](./references/progressive_disclosure.md)
3. **Claude vs. AGY Compatibility**:
   - Follow the cross-compatibility guidelines: [references/claude_vs_agy.md](./references/claude_vs_agy.md)
   - Use provided templates: [templates/custom_skill_template.md](./templates/custom_skill_template.md)

---

## Step 3: Validation & Link Integrity Checking

Run the automated validator to verify frontmatter, schema constraints, and link validity:

```bash
python tools/skill_builder.py validate <skill-name>
```

The validator checks:
- [x] Valid YAML frontmatter delimiters and fields (`name`, `description`).
- [x] `name` matches directory name and naming convention.
- [x] Description length and trigger phrasing.
- [x] Line length warning threshold (progressive disclosure check).
- [x] Resolution of all relative markdown links (`[label](./path/to/file)`).

---

## Step 4: Multi-Agent Synchronization

Keep `.agents/skills/` (AGY) and `.claude/skills/` (Claude) perfectly synchronized:

```bash
python tools/skill_builder.py sync
```

---

## Related References & Templates
- [Claude vs. AGY Architecture Comparison](./references/claude_vs_agy.md)
- [Progressive Disclosure Guide](./references/progressive_disclosure.md)
- [Skill Template](./templates/custom_skill_template.md)
