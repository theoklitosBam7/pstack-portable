# Cursor adapter

## Operation map

| Neutral op | Cursor call |
|---|---|
| ask-user | `AskQuestion` tool, options plus free text |
| todolist | Cursor's built-in todo list tool |
| spawn-subagent | `Task` tool with `subagent_type`, `model`, `run_in_background`, `readonly` |
| persona | plugin's `agents/` directory, already registered. `subagent_type: "poteto-agent"` or `subagent_type: "comment-sicko"` |
| discover-mcps | the available-tools map in the system prompt, else the `mcps/` directory Cursor exposes |
| find-transcripts | `~/.cursor/projects/<slug>/agent-transcripts/<uuid>/<uuid>.jsonl`, `<slug>` is the workspace path with the leading slash dropped and each `/` turned into `-`. The system prompt names the active workspace's directory |
| cloud-run | `Task` with `environment: "cloud"`, `cloud_base_branch` when the worker starts from a non-default pushed branch. `environment: "local"` when it needs this machine |

## Config

`/setup-pstack` writes both `~/.config/pstack/models` and the mirror `~/.cursor/rules/pstack-models.mdc` with `alwaysApply: true`, so the choices inject every session. The `.mdc` mirror is the one Cursor reads automatically.

## Default model roles

Configured lines win. Without config, roles resolve to Cursor slugs: `code` = `gpt-5.6-sol-max`, `fast` = `grok-4.6-fast-xhigh`, `judgment` = `claude-fable-5-thinking-max`, `hardest` = `claude-fable-5-thinking-max`. Panel defaults: `how critics`, `arena runners`, `arena cross-judge pool`, `architect runners`, `interrogate reviewers` = `claude-fable-5-thinking-max`, `gpt-5.6-sol-max`, `grok-4.6-fast-xhigh`, `claude-opus-5-thinking-xhigh`. `how explorer` and `why investigators` and `swarm workers` = `grok-4.6-fast-xhigh`. `how explainer`, `why synthesizer`, `reflect judgment` = `claude-fable-5-thinking-max`. `reflect tooling` = `gpt-5.6-sol-max`. Playbook lines map: `bug-fix`, `perf-issue`, `hillclimb`, `hardest tasks` = `gpt-5.6-sol-max`, with judgment-heavy instances on `claude-fable-5-thinking-max` per the poteto-mode tiering rule.

## Notes

- `Task` model slugs that fail to resolve: read the error's valid slugs, pick the closest equivalent, highest reasoning tier of the same family, and fix the config in a separate PR. `inherit-parent` and `auto` mean omit `model`.
- Cursor built-ins pstack references: `/create-skill` for skill authoring, `/loop` for wake chains, built-in babysit superseded by the pstack playbook of the same name. The `cursor-team-kit` plugin supplies `deslop`, `control-cli`, `control-ui`.
- Detection: Cursor names itself in the system prompt and exposes `AskQuestion` plus `Task`.
