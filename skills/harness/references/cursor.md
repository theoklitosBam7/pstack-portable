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

Model config: `~/.config/pstack/models`.

User-level mirror: `~/.cursor/rules/pstack-models.mdc` with `alwaysApply: true`. [Setup-pstack, step 6](../../setup-pstack/SKILL.md#6-write-the-config) writes the same role mappings to this mirror, which Cursor reads automatically. This mirror completes the models-config setup for Cursor.

## Default model roles

Configured lines win. Without config, `code` and `fast` use `grok-4.7-xhigh-fast`; `judgment` and `hardest` use `claude-opus-5-5-max`. `arena runners`, `arena cross-judge pool`, `architect runners`, and `interrogate reviewers` use `claude-opus-5-5-max`, `gpt-5.6-sol-max`, and `grok-4.7-xhigh-fast`. `how explorer`, `why investigators`, and `swarm workers` use `grok-4.7-xhigh-fast`. `how explainer`, `why synthesizer`, and `reflect judgment` use `claude-opus-5-5-max`. `reflect tooling` uses `gpt-5.6-sol-max`. Playbook lines map: `feature`, `refactoring`, `bug-fix`, `perf-issue`, and `hillclimb` use the `code` role; `hardest tasks` use the `hardest` role.

## Notes

- `Task` model slugs that fail to resolve: read the error's valid slugs, pick the closest equivalent, highest reasoning tier of the same family, and fix the config in a separate PR. `inherit-parent` and `auto` mean omit `model`.
- Cursor built-ins pstack references: `/create-skill` for skill authoring, `/loop` for wake chains, built-in babysit superseded by the pstack playbook of the same name. The `cursor-team-kit` plugin supplies `deslop`, `control-cli`, `control-ui`.
- Detection: Cursor names itself in the system prompt and exposes `AskQuestion` plus `Task`.
