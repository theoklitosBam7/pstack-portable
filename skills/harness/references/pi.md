# pi adapter

## Operation map

| Neutral op | pi call |
|---|---|
| ask-user | none built in. Ask in plain reply text with the options as a list. The example `question` extension adds a structured tool when installed |
| todolist | none built in, by design. Keep a `TODO.md` or a markdown checklist in the reply |
| spawn-subagent | none built in. The official `subagent` extension adds a `subagent` tool with `agent` plus `task`, a `tasks[]` parallel form, and a `chain[]` sequential form. Without it, run the work in the main thread per the fallback policy |
| persona | markdown plus frontmatter, `name`, `description`, `tools`, `model`, in `~/.pi/agent/agents/` or `.pi/agents/`. Copy `agents/poteto-agent.md` and `agents/comment-sicko.md` there |
| discover-mcps | none. pi has no MCP support by design. Name MCP-sourced evidence as unavailable and use CLI tools or the shared record instead |
| find-transcripts | `~/.pi/agent/sessions/--<path>--/<timestamp>_<uuid>.jsonl`. JSONL with a tree structure, `id` and `parentId` per entry |
| cloud-run | none. Use tmux for long local runs and the fallback policy otherwise |

## Config

`~/.config/pstack/models`. `AGENTS.md` is the always-on surface, `~/.pi/agent/AGENTS.md` plus directory walk from cwd. Reference the config path there for per-session loading.

## Default model roles

Without config, every role runs on the session model and the reply says so. Multi-model panels need the subagent extension with per-agent `model` frontmatter, or scoped models via `/scoped-models`.

## Notes

- Unknown frontmatter fields are ignored, stated in the docs.
- Skills load from `~/.pi/agent/skills/`, `~/.agents/skills/`, `.pi/skills/`, `.agents/skills/`, plus the settings `skills` array and `pi install` packages.
- Detection: `AI_AGENT=pi` or `PI_CODING_AGENT=true`. Shell tools also see `PI_SESSION_ID`, `PI_PROVIDER`, `PI_MODEL`.
