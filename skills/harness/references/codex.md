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

Model config: `~/.config/pstack/codex/models`.

User-level instruction file: `~/.codex/AGENTS.md`. Add the exact line from [setup-pstack, step 6](../../setup-pstack/SKILL.md#6-write-the-config) to this file so later sessions read the config before selecting models for pstack roles.

## Reasoning budget

Before each pstack subagent spawn, read the `# Budget:` comment in the Codex model config. Use it as the starting `reasoning_effort`: `unlimited` = `max`, `large` = `xhigh`, `medium` = `high`, and `small` = `medium`. The saved target is a starting point, not a spending limit. For the hardest or subtlest work, raise the effort one step; for judgment work, lower it one step; for routine work, lower it at least two steps. Use the order `low`, `medium`, `high`, `xhigh`, `max`. Keep verification on the starting effort. Preserve the selected role's model, including the parent model for `auto` and `inherit-parent`.

Pass the resulting `reasoning_effort` in the spawn call when the current tool schema permits it. Respect higher-priority instructions and the model's supported effort levels. If the target is unsupported, use the highest supported level no higher than the target and report the fallback. If no supported level is at or below the target, omit the override and report that the budget could not be applied. If the config has no recognized budget, omit the effort override and use the harness default. If the tool does not accept an effort override, omit it and report that the budget could not be applied. Do not infer supported levels or attempt an override the current tool disallows.

## Default model roles

Without config: resolve at setup time from what your account can spawn. `judgment` = the strongest reasoning-effort model, `code` = the strongest default-effort model, `fast` = the fastest acceptable model. Panels: distinct models where available, otherwise sequential passes on one model, stated in the reply.

## Notes

- Unknown frontmatter fields are silently ignored, verified in the parser source. Vendor extras belong in `metadata` per the spec, but top-level extras load fine locally.
- Skills load from `$CWD/.agents/skills` and `$HOME/.agents/skills`.
- Detection: `CODEX_SANDBOX` set is a weak signal, sandboxed runs only. Otherwise fingerprint on `request_user_input` plus `update_plan`.
