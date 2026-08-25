---
name: setup-pstack
description: Configure which models pstack uses per role for the harness you are running in. Detects your available models and writes the portable model config that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", or changing pstack's model choices.
---

# Setup pstack

Write the pstack model config, one line per role, mapping each role to a model you can actually spawn in this harness. The skills read it and fall back to their inline defaults when a line is absent, so this is an override layer, not a requirement.

## Steps

### 1. Detect the harness

Run the detection in the **harness** skill (`../harness/SKILL.md`). Every later step depends on knowing the harness, because model slugs, spawn parameters, and config mirrors are per harness.

### 2. Detect available models

Enumerate the model ids you can pass to a subagent in this session. That is the dependable source. Check the harness adapter for how: Cursor's `Task` tool errors list valid slugs, Claude Code exposes `sonnet`/`opus`/`haiku`/`fable` aliases, opencode and Crush list `provider/model-id` forms, Amp routes through the Dial. If the harness also exposes a models API or CLI, prefer it for completeness. If you cannot detect any, ask the user to paste the ids they have access to. Never write a real id you have not confirmed is available. The aliases `inherit-parent` and `auto` are always valid even though they are not detected ids.

### 3. Load current state

The default role-to-model mapping is the role table in the **harness** skill plus the adapter's default section. If `~/.config/pstack/models` already exists, read it and treat its values as the current choices. Otherwise start from those defaults.

### 4. Map and confirm

Show every role with its current model, marking any real id not in the detected set as needing a choice. Ask whether to accept as-is or change specific roles, offering the detected models plus `inherit-parent` and `auto`, both meaning this role runs on the parent session model, as the options. Use the harness's structured ask-user operation, plain text where the harness has none. For panel roles (`how critics`, `arena runners`, `architect runners`, `interrogate reviewers`) the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena selects one value from it whose model family differs from the parent's when possible. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

### 5. Validate

Every real id written must be in the detected set. `inherit-parent` and `auto` always pass. If a chosen real id is not available, stop and ask again. A config pointing at a model the user cannot use breaks every delegation that reads it.

### 6. Write the config

Write `~/.config/pstack/models`, one line per role, using the same labels poteto-mode uses. Overwrite the whole file so re-runs stay idempotent. Shape:

```
# pstack model configuration. One line per role. Delete a line to fall back to the adapter default.
# `inherit-parent` or `auto` as a value: the role runs on the parent session model. Alias entries in a panel list still count toward its fan-out.
code: <strongest instruction-following model>
fast: <fastest acceptable model>
judgment: <strongest thinking model>
hardest: <strongest model for the hardest tasks>
how explorer: <fast model>
how explainer: <judgment model>
how critics: <list of up to four distinct-family models>
why investigators: <fast model>
why synthesizer: <judgment model>
reflect tooling: <code model>
reflect judgment: <judgment model>
arena runners: <list of up to four distinct-family models>
arena cross-judge pool: <list of up to four distinct-family models>
swarm workers: <fast model>
architect runners: <list of up to four distinct-family models>
interrogate reviewers: <list of up to four distinct-family models>
```

On Cursor, also write the mirror `~/.cursor/rules/pstack-models.mdc` with `alwaysApply: true` and the same lines, so the choices inject every session. On other harnesses, add one line to the always-on context file the adapter names (`AGENTS.md` or equivalent) pointing at `~/.config/pstack/models`, so sessions that never run this skill still find the config.

### 7. Confirm

Tell the user the config was written and that it applies to new sessions. Re-running this skill updates it.

### 8. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof, a `verify-*` skill or an existing harness. If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, invoke `/create-verification-skill`, which resolves wherever pstack is installed. On no, move on without pushing.
