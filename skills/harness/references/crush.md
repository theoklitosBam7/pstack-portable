# Crush adapter

## Operation map

| Neutral op | Crush call |
|---|---|
| ask-user | `question` tool, `questions[]` each with `type` of `yes_no` or `single_choice` or `multi_choice` or `free_text`, `question`, `description`, `choices[]` with id plus label. Free-text fill-in is automatic on choice questions |
| todolist | `todos` tool, one item in progress at a time |
| spawn-subagent | `agent` tool with a single `prompt` param. Read-only toolset only, glob, grep, ls, view. It cannot write. Use it for exploration and review briefs, never for implementation. Implementation stays in the main thread |
| persona | no markdown persona files. Agents are config-defined, `coder` and `task` in crush.json. Paste `agents/poteto-agent.md` or `agents/comment-sicko.md` in full into the brief |
| discover-mcps | `mcp` block in crushrc or crush.json, tools surface as `mcp_<server>_<tool>`. `crush_info` reports MCP status |
| find-transcripts | SQLite `crush.db` in the data directory, default `.crush` per project. Treat direct reads as unavailable, use `crush logs` for run logs |
| cloud-run | none. Background shell exists via bash `run_in_background`, no remote compute. Use the fallback policy |

## Config

Model config: `~/.config/pstack/models`.

User-level instruction file: `~/.config/crush/CRUSH.md`. Add the exact line from [setup-pstack, step 6](../../setup-pstack/SKILL.md#6-write-the-config) to this file so later sessions read the config before selecting models for pstack roles.

## Default model roles

Config defines per-agent `model` as `large` or `small` slots. Without config: `judgment` and `code` = large, `fast` = small. Multi-model means large plus small, so panels cap at two models. State collapsed panels in the reply.

## Notes

- Unknown frontmatter fields are silently ignored, verified in the loader source.
- Skills load from `$CRUSH_SKILLS_DIR`, `~/.config/agents/skills/`, `~/.config/crush/skills/`, `~/.agents/skills/`, `~/.claude/skills/`, and project `.agents/skills/`, `.crush/skills/`, `.claude/skills/`, `.cursor/skills/`.
- Detection: no env var. Fingerprint on the `question` tool shape or `crush_info`.
- The read-only `agent` tool makes Crush the weakest delegation target. Prefer main-thread work with small outputs.
