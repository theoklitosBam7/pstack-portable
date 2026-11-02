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

Model config: `~/.config/pstack/cursor/models`.

User-level mirror: `~/.cursor/rules/pstack-models.mdc` with `alwaysApply: true`. [Setup-pstack, step 6](../../setup-pstack/SKILL.md#6-write-the-config) writes the same role mappings to this mirror, which Cursor reads automatically. This mirror completes the models-config setup for Cursor.

## Reasoning budget

Use the selected role's effort-suffixed model ID as the starting level. Adjust its suffix for the task under the harness budget rules, retaining the family and speed. Use only a model ID confirmed available in the current session. If the adjusted ID is unavailable, use the confirmed same-family ID at the highest effort no higher than the target; if none is confirmed, use the configured ID and report the fallback. Cursor also documents bracketed effort parameters in custom-agent model definitions, but do not assume the live Task call accepts them. `auto` and `inherit-parent` omit `model` and inherit the parent effort; report that the budget cannot set it.

## Default model roles

Configured lines win. Without config, `code` and `fast` use `grok-4.7-xhigh-fast`; `judgment` and `hardest` use `claude-opus-5-5-xhigh`. `arena runners`, `arena cross-judge pool`, `architect runners`, and `interrogate reviewers` use `claude-opus-5-5-xhigh` and `grok-4.7-xhigh-fast`. `how explorer`, `why investigators`, `swarm workers`, and `reflect tooling` use `grok-4.7-xhigh-fast`. `how explainer`, `why synthesizer`, and `reflect judgment` use `claude-opus-5-5-xhigh`. Playbook lines map: `feature`, `refactoring`, `bug-fix`, `perf-issue`, and `hillclimb` use the `code` role; `hardest tasks` use the `hardest` role.

## Notes

- `Task` model slugs that fail to resolve: read the error's valid slugs, pick the closest equivalent, highest reasoning tier of the same family, and fix the config in a separate PR. `inherit-parent` and `auto` mean omit `model`.
- Cursor built-ins pstack references: `/create-skill` for skill authoring, `/loop` for wake chains, built-in babysit superseded by the pstack playbook of the same name. The `cursor-team-kit` plugin supplies `deslop`, `control-cli`, `control-ui`.
- Detection: Cursor names itself in the system prompt and exposes `AskQuestion` plus `Task`.
