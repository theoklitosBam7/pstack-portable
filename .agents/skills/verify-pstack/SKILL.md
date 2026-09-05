---
name: verify-pstack
description: "Drive and prove pstack-portable's user-facing behavior: the ~/.agents/skills install is valid, every skill file loads cold, and the model config parses. Use before claiming a pstack change works, or when a pstack skill misbehaves in a session."
---

# Verify pstack-portable

pstack-portable is a skills collection, not a server. The app is markdown: the files under `skills/`, `agents/`, and `automations/` that harnesses load through the install, plus the model config at `~/.config/pstack/models` that routes roles. A proof here means a real file loaded cold by a fresh agent, or a checker run with its output saved. The feature map in `features/` is the maintained list of what to drive.

## Launch

Nothing starts. The instance is this checkout plus the machine's install state. Readiness:

- `python3 --version` prints a version. The checker needs the standard library only.
- From the repo root, `python3 .agents/skills/verify-pstack/verify.py doctor` prints `doctor: ok`. The script finds the repo from its own path, so it runs from anywhere.

Teardown: no process exists, so there is nothing to stop. Concurrent runs are safe because every drive is read-only; give each run its own `RUN_ID` evidence directory.

## Doctor

`verify.py doctor` answers "is this install worth driving?" It is read-only and checks:

- checkout shape: `skills/` and `agents/` exist at the repo the script belongs to,
- install: every `skills/` directory has an entry in `~/.agents/skills/`; manual installs require symlinks that resolve inside this checkout, while Skills CLI installs require `~/.agents/.skill-lock.json` to record every skill from `theoklitosBam7/pstack-portable`,
- model config: every non-comment line parses as `role: value`, roles come from the table in `skills/setup-pstack/SKILL.md`, panel list entries are non-empty.

Exit 0 prints `doctor: ok`. `FAIL` lines name the section and include the fix (the README's install command, or re-running `/setup-pstack`). Run doctor before the first drive of a run, and again after any failed drive. A verification run reports doctor failures; it never repairs the install itself. Repair is a setup action for the user.

## Drive

Two drives, static then live. Static first; it is cheap and finds most drift.

### Static: checker

```bash
# from the repo root
python3 .agents/skills/verify-pstack/verify.py check
```

`check` audits frontmatter (`name`, `description`) on every `SKILL.md` under `skills/` and `automations/` and on `agents/*.md`, then resolves every relative markdown link in those files plus `README.md` and `docs/**/*.md`. Exit 0 prints `check: ok` with counts. `FAIL` lines carry `path:line`.

### Live: cold load

Spawn one fresh subagent per skill under test. On pi, use the installed `subagent` extension with its `agent` and `task` fields. On other harnesses, use the spawn-subagent operation in the `harness` skill. Do not assume a built-in agent name. The brief template, with the absolute path filled in:

```text
Read the file at <ABSOLUTE PATH> completely before anything else. Using only that file, answer:
1. Quote, word for word, the frontmatter description.
2. In one sentence, what does the file say to do first when the skill fires?
3. Name one other file this skill points at, with the path exactly as written.
Do not open any other file. Reply with three numbered answers.
```

Then prove the reply against the disk:

```bash
rg -F "<answer 1 quote>" <ABSOLUTE PATH>   # expect exactly one match
test -f "<skill dir>/<answer 3 path without any #fragment>" && echo exists
```

A verbatim quote proves the file loaded. A paraphrase is a fail. Do not tell the subagent it is being verified.

### Isolation

Everything a drive touches is read-only: repo files, symlink farm, model config. Never edit skill files, repair links, or write the config from a verification run. Report the drift and hand back the fix command. Two runs may proceed side by side with distinct `RUN_ID`s.

## Evidence

Write to `.agents/skills/verify-pstack/evidence/<RUN_ID>/<feature>/`, one markdown file per proof, each containing the date, the exact command or brief, the full output or reply, and the confirmation line (`rg -F` match, `test -f` result). Capture the action and the resulting state, not only the final verdict. Record the feature ID and the entry point used. Report an unreachable path with the attempted command and the unmet precondition; do not report a skipped entry point as verified through a different path.

## Cleanup

No process to stop, so never kill by name or pattern; there is nothing running. Cleanup removes nothing except scratch files created outside the evidence directory. Evidence survives cleanup by rule: after cleanup, list the evidence directory and confirm the artifacts are still there. A cleanup that eats the proof fails the run.

## Helpers

`verify.py` (executable) is the only helper:

```bash
python3 .agents/skills/verify-pstack/verify.py doctor   # quick install + config health
python3 .agents/skills/verify-pstack/verify.py check    # full frontmatter + link audit
```

Both are read-only and exit 0 on pass, 1 with `FAIL` lines. `doctor` also prints `note:` lines for healthy fallbacks worth knowing and `warning:` lines for suspicious but non-failing state.
