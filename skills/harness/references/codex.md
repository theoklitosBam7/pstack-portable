# Codex CLI adapter

## Operation map

| Neutral op | Codex call |
|---|---|
| ask-user | `request_user_input`, `questions[]` with `header`, `question`, `options[]` of `label` plus `description`. Free-form is added automatically |
| todolist | `update_plan` |
| spawn-subagent | `spawn_agent` with `message`, `agent_type`, `model`, `reasoning_effort`. `fork_context: none` for standalone briefs. `send_input` and `wait` drive the child. Experimental, so check availability at runtime |
| persona | TOML agent roles in `$CODEX_HOME/agents/` or `[agent_roles.<name>]` in `config.toml`. No markdown personas, so paste `agents/poteto-agent.md` or `agents/comment-sicko.md` into the brief instead |
| discover-mcps | `codex mcp list`, in-session `/mcp`, or `[mcp_servers.<name>]` in `~/.codex/config.toml` |
| find-transcripts | `~/.codex/sessions/YYYY/MM/DD/rollout-<ts>-<uuid>.jsonl`. The first line's `session_meta` holds the cwd |
| cloud-run | `codex cloud` for long-running remote tasks |

## Config

Model config: `~/.config/pstack/models`.

User-level instruction file: `~/.codex/AGENTS.md`. Add the exact line from [setup-pstack, step 6](../../setup-pstack/SKILL.md#6-write-the-config) to this file so later sessions read the config before selecting models for pstack roles.

## Default model roles

Without config: resolve at setup time from what your account can spawn. `judgment` = the strongest reasoning-effort model, `code` = the strongest default-effort model, `fast` = the fastest acceptable model. Panels: distinct models where available, otherwise sequential passes on one model, stated in the reply.

## Notes

- Unknown frontmatter fields are silently ignored, verified in the parser source. Vendor extras belong in `metadata` per the spec, but top-level extras load fine locally.
- Skills load from `$CWD/.agents/skills` and `$HOME/.agents/skills`.
- Detection: `CODEX_SANDBOX` set is a weak signal, sandboxed runs only. Otherwise fingerprint on `request_user_input` plus `update_plan`.
