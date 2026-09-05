# Goose adapter

## Operation map

| Neutral op | Goose call |
|---|---|
| ask-user | none documented. Ask in plain chat text with options as a markdown list |
| todolist | `todo_write` |
| spawn-subagent | `delegate` tool with `source`, `instructions`, optional `model` and `max_turns`. Background with `async: true`, then `load(taskId)` to wait and `load(..., cancel: true)` to stop. Defaults cap at five concurrent background tasks |
| persona | markdown plus frontmatter, `name` required, in `~/.agents/agents/` or `<project>/.agents/agents/`. Copy `agents/poteto-agent.md` and `agents/comment-sicko.md` there |
| discover-mcps | extensions in `~/.config/goose/config.yaml`. Tools surface as `<extension>__<tool>`. `goose info -v` lists enabled extensions |
| find-transcripts | SQLite `sessions.db` since v1.10.0, location from `goose info`. Legacy JSONL under `~/.config/goose/sessions/`. Export with `goose session export` |
| cloud-run | none managed. `goose run` is headless local. Use the fallback policy |

## Config

Model config: `~/.config/pstack/models`.

User-level instruction file: `~/.config/goose/.goosehints`. Add the exact line from [setup-pstack, step 6](../../setup-pstack/SKILL.md#6-write-the-config) to this file so later sessions read the config before selecting models for pstack roles.

## Default model roles

`delegate` takes a `model` override. Without config: `judgment` = the strongest configured provider model, `fast` = `GOOSE_FAST_MODEL` or the fastest acceptable, `code` = the active model. `GOOSE_PLANNER_MODEL` covers plan-mode work.

## Notes

- Unknown frontmatter fields are silently ignored, verified in the parser source. Arbitrary extras belong under `metadata`.
- Skills load from `~/.agents/skills/`, `.agents/skills/`, plugins via `goose plugin install <git-url>`, plus compat `.goose/skills/` and `.claude/skills/`.
- Detection: `AGENT_SESSION_ID` is set in shell subprocesses but marks any agent session, not Goose specifically. Fingerprint on `delegate` plus `load`.
