---
name: setup-pstack
description: Configure which models pstack uses for each role and set a reasoning budget. Detects models available in the active harness and writes the portable model config. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# Setup pstack

Write the pstack model config at `~/.config/pstack/models`. Use one line per role. Map each role to a model available in the active harness. The skills read this file and use adapter defaults for roles without a line.

## Steps

### 1. Detect the harness

Run detection from the **harness** skill (`../harness/SKILL.md`). Read that harness's adapter. Model IDs, subagent options, and config mirrors vary by harness.

### 2. Detect available models

Use the active harness to list models that subagents can use. Check the adapter for the right operation. If the harness has a model API or CLI, use it to check availability. If you cannot list models, ask the user to provide the available model IDs. Never write an unconfirmed model ID. `inherit-parent` and `auto` are always valid aliases.

### 3. Load the current state

Read `~/.config/pstack/models` if it exists. Keep its role values and the recorded budget as the current choices. Otherwise use the role defaults in the **harness** skill and the active adapter.

The `how critics` role is no longer used. When the current config has that line, report it as retired and omit it from the new config.

### 4. Choose a reasoning budget

Use the harness's ask-user operation. Offer these choices and include the current budget when the config records one:

- `unlimited` to keep the highest available reasoning level.
- `large` for `xhigh` reasoning.
- `medium` for `high` reasoning.
- `small` for `medium` reasoning.

Build the role table from the harness defaults and current config. On a rerun, keep each role's model family, panel membership, or alias. Change only the reasoning level unless the user asks for another model.

For model IDs that use effort suffixes, apply the selected level to every real ID, including panel entries. The effort order is `max`, `xhigh`, `high`, `medium`, then `low`. The effort suffix is the last token, or the token before a trailing `fast`.

Use only IDs from the detected model list. If the target ID is unavailable, choose a detected ID from the same family at the highest level that does not exceed the target. If no such ID exists, ask the user to choose from the detected list. Do not make up a model ID.

Some harnesses use model IDs that do not show an effort suffix. Keep those IDs unchanged and tell the user that the selected budget cannot change their reasoning level. `inherit-parent` and `auto` also stay unchanged because they use the parent session model.

### 5. Review and confirm the role table

Show every role and its model. Mark any ID that is not in the detected list as needing a choice. State which roles could not use the selected budget, and list any retired config lines that you will omit.

Ask whether the user accepts the table or wants to change specific roles. Offer detected models, `inherit-parent`, and `auto`. Both aliases mean that the role uses the parent session model. Use the harness's ask-user operation. For panels (`arena runners`, `architect runners`, and `interrogate reviewers`), the value is a list. One subagent runs per entry, so the list length sets the panel size. `arena cross-judge pool` is a list from which Arena picks a model family that differs from the parent's when possible. `swarm workers` is the default for workers unless a race or comparison assigns a model to each arm.

### 6. Write the config

Check that every real model ID is in the detected list. `inherit-parent` and `auto` are valid aliases. If an ID is unavailable, stop and ask the user to choose again.

Write `~/.config/pstack/models`, one line per role. Overwrite the file so reruns remove retired roles and stay idempotent. Record the selected budget in a comment. The comment is not a model role.

```text
# pstack model configuration. Delete a role line to use its adapter default.
# Budget: medium (high reasoning)
# `inherit-parent` and `auto` use the parent session model.
code: <strongest instruction-following model>
fast: <fastest acceptable model>
judgment: <strongest reasoning model>
hardest: <strongest model for the hardest tasks>
how explorer: <fast model>
how explainer: <reasoning model>
why investigators: <fast model>
why synthesizer: <reasoning model>
reflect tooling: <code model>
reflect judgment: <reasoning model>
arena runners: <list of distinct-family models>
arena cross-judge pool: <list of distinct-family models>
swarm workers: <fast model>
architect runners: <list of distinct-family models>
interrogate reviewers: <list of distinct-family models>
```

On Cursor, also write the same role mappings and budget comment to `~/.cursor/rules/pstack-models.mdc`. Add this frontmatter before the config:

```yaml
---
description: pstack model and reasoning budget
alwaysApply: true
---
```

On other harnesses, use the exact user-level instruction file named in the adapter's Config section. Preserve its existing instructions. Add this line once, or update the existing pstack config instruction:

```text
Before selecting models for pstack roles, read `~/.config/pstack/models` if it exists.
```

### 7. Confirm the result

Tell the user which config and instruction or mirror files you wrote. State the chosen budget and name any role whose model ID could not apply it.

### 8. Offer a verification skill

Check whether the project has a way to drive the real app for proof, such as a `verify-*` skill or an existing harness. If it does not, offer once to create a project-local verification skill. On yes, invoke `/create-verification-skill`. On no, continue without asking again.
