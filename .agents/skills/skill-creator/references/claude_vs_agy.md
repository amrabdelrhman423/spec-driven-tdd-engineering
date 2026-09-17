# Claude vs. AGY Skill Architecture Comparison

Both Anthropic Claude and Google Antigravity (AGY) are top-tier AI coding agents that support modular customization, but they have subtle ecosystem differences.

---

## Comparison Matrix

| Dimension | Google Antigravity (AGY) | Anthropic Claude (Claude Code) | Universal Standard in this Repo |
| :--- | :--- | :--- | :--- |
| **Skill Location** | `.agents/skills/<name>/SKILL.md` (or `~/.gemini/config/skills/`) | `.claude/skills/<name>/SKILL.md` or CLAUDE.md index | Dual-mirrored in `.agents/` and `.claude/` via `sync` |
| **Trigger Mechanism** | Model decision based on `description` in YAML frontmatter | Slash commands, CLAUDE.md instructions, or autonomous tool invocation | Standard YAML frontmatter with third-person trigger ("Use this skill when...") |
| **Directives File** | `AGENTS.md` and `GEMINI.md` | `CLAUDE.md` | Root `AGENTS.md` and `CLAUDE.md` cross-referencing each other |
| **Progressive Disclosure** | Reads `SKILL.md` on demand; reads `references/` only when needed | Ingests linked markdown docs upon navigation | Compact `SKILL.md` with relative links to `references/` |
| **Tool Calling** | Built-in CLI tools + MCP (JSON schema) | Claude bash tool + MCP | Cross-platform Python/shell helpers |

---

## Best Practice for Cross-Compatibility

1. **Always use YAML frontmatter** with `name` and `description`.
2. **Keep descriptions trigger-focused**: Never write generic summaries like "This handles files". Write "Use this skill when the user asks to format, lint, or restructure JSON datasets."
3. **Use standard relative markdown links**: E.g. `[guide](./references/guide.md)`. Both Claude and AGY resolve these cleanly.
4. **Avoid platform-specific shell quirks**: Write scripts in Python or cross-platform PowerShell/Bash.
