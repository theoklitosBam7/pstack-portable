# opencode adapter

## Operation map

| Neutral op | opencode call |
|---|---|
| ask-user | `question` tool, options plus a free-form fallback, `multiple: true` when needed |
| todolist | `todowrite` |
| spawn-subagent | `task` tool with `description`, `prompt`, `subagent_type`. Background with `background: true`, which needs `OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS=true`. Built-ins: `general`, read-only `explore` and `scout` |
| persona | markdown in `.opencode/agents/` or `~/.config/opencode/agents/` with frontmatter `description`, `mode`, `model`, `tools`. Copy `agents/poteto-agent.md` and `agents/comment-sicko.md` there, mapped to this frontmatter |
| discover-mcps | the `mcp` key in opencode.json. Tools surface as `<server>_<tool>` |
| find-transcripts | `~/.local/share/opencode/storage/`, per-entity JSON plus `opencode.db` SQLite |
| cloud-run | none managed. `opencode serve` or SDK runs exist, but use local worktrees and the fallback policy |

## Config

`~/.config/pstack/models`. `AGENTS.md` is the always-on surface, project plus `~/.config/opencode/AGENTS.md`. Reference the config path there for per-session loading.

## Default model roles

Agents take `model` as `provider/model-id` in config. Without config: `judgment` = the strongest model on the strongest provider, `fast` = a flash-class model, `code` = the strongest default tier. Different agents in one session may use different models, so panels fan out for real.

## Notes

- Unknown frontmatter fields are ignored, stated in the docs.
- Skills load from `.opencode/skills/`, `~/.config/opencode/skills/`, and the compat paths `.claude/skills/`, `~/.claude/skills/`, `.agents/skills/`, `~/.agents/skills/`.
- Detection: `OPENCODE=1`, `AGENT=1`, `OPENCODE_PID` in the process environment.
