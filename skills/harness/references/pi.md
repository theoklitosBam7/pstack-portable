# pi adapter

## Operation map

| Neutral op | pi call |
|---|---|
| ask-user | none built in. Ask in plain reply text with the options as a list. The example `question` extension adds a structured tool when installed |
| todolist | none built in, by design. Keep a `TODO.md` or a markdown checklist in the reply |
| spawn-subagent | none built in. Inspect the installed extension's tool schema and instructions for dispatch, parallel calls, and results. If no suitable tool is available, use the fallback policy |
| persona | use the installed extension's documented persona format and locations. If it does not support personas, paste the persona into the brief |
| discover-mcps | inspect available tools and installed extensions for MCP discovery. If unavailable, name MCP-sourced evidence as unavailable and use CLI tools or the shared record instead |
| find-transcripts | `~/.pi/agent/sessions/--<path>--/<timestamp>_<uuid>.jsonl`. JSONL with a tree structure, `id` and `parentId` per entry |
| cloud-run | none. Use tmux for long local runs and the fallback policy otherwise |

## Config

Model config: `~/.config/pstack/pi/models`.

User-level instruction file: `~/.pi/agent/AGENTS.md`. Add the exact line from [setup-pstack, step 6](../../setup-pstack/SKILL.md#6-write-the-config) to this file so later sessions read the config before selecting models for pstack roles.

## Reasoning budget

Pi has no built-in subagent tool. Check the active extension's instructions and live tool schema for per-call reasoning controls and any restrictions on their use. Apply the shared budget rules using a confirmed model-supported value when permitted. Otherwise leave the existing effort setting in effect and report that the saved budget could not be applied. Do not modify shared agent files to simulate a per-call override.

## Default model roles

Use the shared role resolution rules. Check the active extension's instructions and live tool schema for model selection, inheritance, and any restrictions on overrides. Apply the resolved role model when permitted. For `auto`, `inherit-parent`, or an unresolved role, select the session model using the extension's documented mechanism; omitting a model may instead select an agent-specific default. If the requested model or parent inheritance cannot be applied, report the actual fallback and state when a panel collapses to one model.

## Notes

- Skills load from `~/.pi/agent/skills/`, `~/.agents/skills/`, `.pi/skills/`, `.agents/skills/`, plus the settings `skills` array and `pi install` packages.
- Detection: `AI_AGENT=pi` or `PI_CODING_AGENT=true`. Shell tools also see `PI_SESSION_ID`, `PI_PROVIDER`, `PI_MODEL`.
