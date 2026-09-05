# Amp adapter

## Operation map

| Neutral op | Amp call |
|---|---|
| ask-user | none built in. Ask in plain chat text with options as a markdown list |
| todolist | none, the tool was removed. Keep a markdown checklist in the reply |
| spawn-subagent | built-in specialists `Review`, `Search`, `Oracle`, `Librarian` are auto-delegated with isolated context. No user-defined markdown personas, so custom roles only via the plugin API `amp.createAgent({ name, model, instructions, tools })` |
| persona | no markdown persona support. Paste `agents/poteto-agent.md` or `agents/comment-sicko.md` in full at the top of the subagent brief or plugin-agent instructions |
| discover-mcps | `amp mcp doctor` for status, config under `amp.mcpServers` in `~/.config/amp/settings.json` and `.amp/settings.json` |
| find-transcripts | on-disk location undocumented. Treat as unavailable and apply the fallback policy |
| cloud-run | Orbs, per-thread cloud machines, `amp -ox "<prompt>"`. Automations schedule thread wake-ups |

## Config

Model config: `~/.config/pstack/models`.

User-level instruction file: `~/.config/amp/AGENTS.md`. Add the exact line from [setup-pstack, step 6](../../setup-pstack/SKILL.md#6-write-the-config) to this file so later sessions read the config before selecting models for pstack roles.

## Default model roles

Amp routes models itself through the Dial, `low` to `ultra`. Model choice per subagent is mostly automatic, so treat roles as hints: `judgment` work asks for the highest dial, `fast` work accepts the default. Plugin agents pin exact models when needed.

## Notes

- Frontmatter tolerance is undocumented. Amp reads Claude-compatible skill dirs, which suggests leniency, but keep frontmatter minimal if a skill fails to load.
- Skills load from `~/.config/agents/skills/`, `~/.agents/skills/`, `~/.config/amp/skills/`, `.agents/skills/`, plus `.claude/skills/` and `~/.claude/skills/`. Install third-party with `amp skill add <git-url> --global`.
- Detection: no env var documented. Fingerprint on the built-in specialist tools.
