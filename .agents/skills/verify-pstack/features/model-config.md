# Model config

`/setup-pstack` writes `~/.config/pstack/models`, one `role: model` line per role, and every pstack skill reads it to route subagents. A missing line falls back to the session model, and `auto` or `inherit-parent` also means the session model.

## Sub-features

- `config-format`: every non-comment line parses as `role: value`.
- `config-roles`: role names come from the table in `skills/setup-pstack/SKILL.md`.
- `config-resolve`: panel values may be comma-separated lists; `auto` and `inherit-parent` entries are always legal.

## How to get to it (user POV)

- Run `/setup-pstack` in a session, pick mappings per role, and the file appears. It applies to new sessions; re-running updates it.
- Delete a line to fall back to the adapter default for that role.

## Driving it with pi

Preconditions:

- doctor has run this session (its config section is the format and role audit).

- Format and role audit, expect `doctor: ok` or `FAIL` lines with line numbers: `python3 .agents/skills/verify-pstack/verify.py doctor`
- Role source of truth, expect each configured role name to appear in the setup skill: `rg -n "how critics|arena runners|interrogate reviewers" skills/setup-pstack/SKILL.md`
- Live resolution, expect every listed agent to show `source: inherits current session model` while the config maps roles to `auto`: call `subagent({ action: "models" })` (pi) and save the output to evidence.

## Gotchas

- Do not write the config during a verification run. Changing routing mid-run invalidates earlier evidence.
- Panel values with `auto` still count fan-out per entry: `auto, auto` spawns two subagents on the same model.
- The checker cannot confirm a model id actually spawns. Id reality needs the harness models API; on pi that is `subagent({ action: "models" })`, which is also the live resolution proof above.
