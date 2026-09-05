# Factory Droid adapter

## Operation map

| Neutral op | Droid call |
|---|---|
| ask-user | `AskUser`, interactive sessions only. It is disabled inside subagents |
| todolist | `TodoWrite` |
| spawn-subagent | `Task` tool with `subagent_type`, `description`, `prompt`, `complexity` of `light` or `medium` or `heavy`, `run_in_background` returning a `task_id`. Retrieve with `TaskOutput` (`block` true or false), stop with `TaskStop`. Built-ins: `worker`, read-only `explorer` |
| persona | markdown plus frontmatter in `<repo>/.factory/droids/` or `~/.factory/droids/`, fields `name`, `description`, `model`, `reasoningEffort`, `tools`. Copy `agents/poteto-agent.md` and `agents/comment-sicko.md` there, mapped to this frontmatter |
| discover-mcps | `mcp.json` at `~/.factory/`, `.factory/`, in-session `/mcp`, or `droid mcp list` |
| find-transcripts | sessions are local and searchable via `droid search`, but the on-disk format is undocumented. Treat file reads as unavailable and use `droid search` |
| cloud-run | Droid Computers, managed cloud machines or BYOM via `droid computer register`. Missions orchestrate multi-agent runs |

## Config

Model config: `~/.config/pstack/models`.

User-level instruction file: `~/.factory/AGENTS.md`. Add the exact line from [setup-pstack, step 6](../../setup-pstack/SKILL.md#6-write-the-config) to this file so later sessions read the config before selecting models for pstack roles.

## Default model roles

Subagents accept `complexity` routing and per-droid `model` frontmatter, `inherit` or an id or `custom:<id>`. Without config: `judgment` = the heaviest complexity tier on the strongest model, `code` = medium tier on the default model, `fast` = light tier. Panels fan out for real with distinct droid models.

## Notes

- Frontmatter tolerance for unknown fields is undocumented. It recognizes several extras including `disable-model-invocation`, so the pstack extras load, but keep an eye on `/skills` status if something shows `Invalid`.
- Skills load from `.factory/skills/`, `~/.factory/skills/`, plus `.agents/skills/` and `~/.agents/skills/`.
- Detection: no env var documented. Fingerprint on `AskUser` plus `TaskOutput`.
- Subagents run non-interactively, no AskUser inside them, and cannot nest.
