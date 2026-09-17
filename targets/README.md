# Agent Targets Architecture

SDE is designed to run with multiple AI agent runtimes without tight platform coupling.

---

## Supported Agent Targets

1. **Google Antigravity (AGY)**:
   - Root configuration: `GEMINI.md` and `AGENTS.md`
   - Customization directory: `.agents/skills/`
   - Runtime model: Injects YAML frontmatter trigger into system prompt; loads `SKILL.md` dynamically on intent match.
2. **Anthropic Claude (Claude Code)**:
   - Root configuration: `CLAUDE.md` and `AGENTS.md`
   - Skills directory: `.claude/skills/` (synchronized from `.agents/skills/` via `tools/skill_builder.py sync` or `sde skill sync`)
   - Directives: Project-level CLI commands and workflow guidelines.
3. **Future Targets**:
   - OpenAI Codex / Custom Agents: Governed by standard `AGENTS.md` and `.specify/constitution.md`.
