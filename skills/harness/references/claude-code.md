# Claude Code adapter

## Operation map

| Neutral op | Claude Code call |
|---|---|
| ask-user | `AskUserQuestion` |
| todolist | `TaskCreate` / `TaskUpdate` / `TaskList` (`TodoWrite` on older builds) |
| spawn-subagent | `Agent` tool with `subagent_type`, per-invocation `model`, `run_in_background` for background mode. Built-in read-only types: `Explore`, `Plan` |
| persona | markdown plus frontmatter in `.claude/agents/` or `~/.claude/agents/`, fields `description`, `model`, `tools`. Copy `agents/poteto-agent.md` and `agents/comment-sicko.md` there, or paste the file into the brief |
| discover-mcps | `claude mcp list`, in-session `/mcp`, or tool names of the form `mcp__<server>__<tool>` |
| find-transcripts | `~/.claude/projects/<munged-cwd>/<session-id>.jsonl`, one JSON object per line |
| cloud-run | `Agent` with `run_in_background`, or `claude --cloud` for remote sessions. No Cursor-style per-agent cloud environments |

## Config

`~/.config/pstack/models` is the source of truth. There is no always-applied rules file to mirror into; if you want the roles injected each session, import the config from `CLAUDE.md` or note the file in `~/.claude/CLAUDE.md`.

## Default model roles

Claude Code aliases: `sonnet`, `opus`, `haiku`, `fable`. Without config: `code` and `hardest` = the strongest instruction-following model you can spawn, `judgment` = the strongest thinking model, `fast` = `haiku`. Panels = the distinct families you can spawn, at most four. Run `/setup-pstack` to write real slugs.

## Notes

- Unknown SKILL.md frontmatter fields are tolerated locally. The claude.ai upload path rejects non-spec keys, so strip `mode`, `icon`, `color`, `reminder` before uploading there.
- Detection: `CLAUDECODE=1` in every subprocess.
- Custom agents support `model`, `tools`, `permissionMode`, `mcpServers`, `effort` in frontmatter.
