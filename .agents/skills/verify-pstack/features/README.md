# pstack verification map

This directory is the maintained source for verifying the user-facing behavior of pstack-portable. The app is the skill files a harness loads, the install that exposes them, and the model config that routes roles. Read this index before driving, then use the matching feature file as the recipe.

## Baseline preconditions

- Commands in this map run from the repo root, meaning the checkout of this repository. The checkout stays the symlink target; never verify a copied tree.
- Every drive is read-only. A verification run never edits skill files, never repairs the install, and never writes `~/.config/pstack/models`. Repair is a setup action (`/setup-pstack`, the install command), not a proof.
- Pick a unique `RUN_ID` (date plus slug, for example `2026-08-29-skillload`) and write evidence to `.agents/skills/verify-pstack/evidence/<RUN_ID>/`.
- `python3` is on `PATH` for the checker.
- Run `verify.py doctor` (see the skill body) before the first drive of the run. Green doctor or no drive; if doctor fails on real install drift, record the finding and drive the features that do not depend on it.

## Driving conventions

- Treat every command as literal. Keep quoted names and flags unchanged.
- Static checks run through `verify.py`. Live drives spawn a cold subagent per the harness skill's spawn-subagent operation; on pi that is the `subagent` tool's `runs.run`.
- A live brief never names this verification run, the word "verify", or this feature map. The subagent reads the target file cold, exactly as a harness session would.
- Quote checks use `rg -F` against the real file. A paraphrase proves nothing.
- Report an unreachable path with the attempted command and the unmet precondition.

## Proof and skip reporting

- Capture the command or brief plus the resulting output, not only the final verdict.
- Static proof: the checker's stdout, saved verbatim.
- Live proof: the exact brief, the subagent's reply, and the `rg -F` line that confirms the quote exists in the file.
- Record the feature ID and entry point used with every artifact.
- Do not report a skipped entry point as verified through a different path.

## Feature entry contract

Each feature file starts with an H1 title and one paragraph describing the user-visible behavior. It then uses exactly four H2 sections in this order.

1. `Sub-features` lists short IDs with one line for each behavior.
2. `How to get to it (user POV)` lists every user entry point.
3. `Driving it with pi` starts with `Preconditions:` and uses labeled bullets that pair each user action with an exact command and observable result.
4. `Gotchas` lists traps that can waste or invalidate a verification run.

Keep implementation details out of the map. Name only user paths, stable handles, required state, commands, and observable proof.

## Features

- [Install](./install.md) covers the `~/.agents/skills/` link farm: completeness, symlink form, and targets inside the checkout.
- [Model config](./model-config.md) covers `~/.config/pstack/models`: line format, role names, and live role resolution.
- [Skill load](./skill-load.md) covers cold loading: frontmatter registration, link integrity, and a fresh agent quoting a real file.
- [poteto-mode routing](./poteto-mode-routing.md) covers playbook links and a cold agent matching a task to a playbook.
- [Personas](./personas.md) covers the two shipped subagent personas: frontmatter, links, and install drift.
