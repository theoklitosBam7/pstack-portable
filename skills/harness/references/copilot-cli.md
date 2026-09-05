# GitHub Copilot CLI adapter

## Operation map

| Neutral op | GitHub Copilot CLI call |
|---|---|
| ask-user | `ask_user`. If disabled by `--no-ask-user`, ask in plain text using the fallback policy |
| todolist | `update_todo` when exposed. Otherwise keep a Markdown checklist in the reply |
| spawn-subagent | `task` with `agent_type` selecting a built-in or custom agent. Use the live tool schema for the brief, model selection, and background execution. `read_agent` checks progress, `list_agents` lists agents, and `write_agent` sends follow-up messages. For read-only exploration use `explore`; for code review use `code-review` |
| persona | Personal definitions in `~/.copilot/agents/<name>.agent.md`, or project definitions in `.github/agents/<name>.agent.md`. Convert `agents/poteto-agent.md` and `agents/comment-sicko.md` to this format, preserving the prompt, `name`, and `description`. Use supported `model` and `tools` fields as needed; omit `is_background`. Restrict Comment Sicko to read-only tools. If custom agents are unavailable, put the persona prompt at the start of the subagent brief |
| discover-mcps | `copilot mcp list`, in-session `/mcp`, or the exposed MCP tools. User config is `~/.copilot/mcp-config.json`; project config can be `.mcp.json` or `.github/mcp.json` |
| find-transcripts | `~/.copilot/session-state/<session-id>/events.jsonl`. Use `COPILOT_AGENT_SESSION_ID` when available to identify the current session. Read event logs without changing them |
| cloud-run | `/delegate` sends work to GitHub's cloud agent and creates a pull request. Use it only when the request authorizes that remote work. Otherwise use local subagents and the fallback policy |

## Config

Model config: `~/.config/pstack/models`.

User-level instruction file: `~/.copilot/copilot-instructions.md`. If `COPILOT_HOME` is set, use `$COPILOT_HOME/copilot-instructions.md` instead. Add the exact line from [setup-pstack, step 6](../../setup-pstack/SKILL.md#6-write-the-config) to this file so later sessions read the config before selecting models for pstack roles.

`COPILOT_HOME` also replaces `~/.copilot` in the agent, MCP, and transcript paths above. The pstack model config stays at `~/.config/pstack/models`. Custom instructions must be enabled for the config-reading instruction to load.

## Default model roles

Use `/model` to inspect available session models and `/subagents` to inspect subagent model choices. Confirm each role's model against the active tool schema or custom agent configuration before saving it. For `inherit-parent`, use the session model and check that the selected agent profile or `/subagents` setting does not supply a different model. Copilot's own Auto routing can override agent model choices; it is not the pstack `auto` alias for the session model.

Without config, use the session model. If per-subagent model selection is unavailable, apply the harness fallback and state that the panel uses one model.

## Notes

- Detection: `COPILOT_CLI=1` in CLI subprocesses, or the combination of `task`, `read_agent`, `list_agents`, and `write_agent`. Use adapter key `copilot-cli`.
- Personal skills load from `~/.agents/skills/` or `~/.copilot/skills/`. Project skills load from `.github/skills/`, `.agents/skills/`, or `.claude/skills/`. The shared pstack install works directly. Use `copilot skill list` to check discovery and `/skills reload` to refresh an interactive session.
- Use the live tool schemas. Optional background and model parameters can differ between CLI versions.

## Sources

- [CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)
- [Configuration directory](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference)
- [Custom agent configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Built-in agents](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents)
- [Skill installation](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)
- [Hook tool mapping](https://docs.github.com/en/copilot/reference/hooks-reference)
- [CLI changelog](https://github.com/github/copilot-cli/blob/main/changelog.md)
