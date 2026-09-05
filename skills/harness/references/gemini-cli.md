# Gemini CLI adapter

## Operation map

| Neutral op | Gemini CLI call |
|---|---|
| ask-user | `ask_user`, `questions[]` with `question`, `header`, `type` of `choice` or `text` or `yesno`, `options[]` with `label` plus `description` |
| todolist | `write_todos`, items with `description` and `status` |
| spawn-subagent | each subagent is exposed as a tool named after it, forced with an `@name` prefix. Built-ins include `generalist` and `codebase_investigator`. Background is not per-spawn, so run fan-outs as sequential or parallel invocations of the subagent tools |
| persona | markdown plus frontmatter in `.gemini/agents/` or `~/.gemini/agents/`, fields `name`, `description`, `model`, `tools`, `temperature`. Copy `agents/poteto-agent.md` and `agents/comment-sicko.md` there, mapped to this frontmatter |
| discover-mcps | `mcpServers` in `~/.gemini/settings.json` or `.gemini/settings.json`, in-session `/mcp`, or the `list_mcp_resources` tool |
| find-transcripts | `~/.gemini/tmp/<project_hash>/chats/`, structured JSON chunks |
| cloud-run | none. Use local worktrees and the fallback policy |

## Config

Model config: `~/.config/pstack/models`.

User-level instruction file: `~/.gemini/GEMINI.md`. Add the exact line from [setup-pstack, step 6](../../setup-pstack/SKILL.md#6-write-the-config) to this file so later sessions read the config before selecting models for pstack roles.

## Default model roles

Without config: per-subagent `model` frontmatter defaults to `inherit`, meaning the session model. Set distinct models per persona when the account allows, `judgment` = the strongest thinking tier, `fast` = flash-class. State collapsed panels in the reply.

## Notes

- Unknown frontmatter fields are silently ignored, verified in the loader source.
- Skills load from `~/.gemini/skills/`, `~/.agents/skills/`, `.gemini/skills/`, `.agents/skills/`. Activation goes through the `activate_skill` tool with a consent dialog on first use.
- Detection: no env var. Fingerprint on `ask_user` plus `write_todos`, or the session context line "This is the Gemini CLI".
