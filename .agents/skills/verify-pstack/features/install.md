# Install

A harness session can load every pstack skill by its slash name because `~/.agents/skills/` holds one symlink per `skills/` directory and each symlink resolves into this checkout. Skills reference their own files and each other by relative path, so a copy instead of a symlink silently breaks them.

## Sub-features

- `install-complete`: every directory under `skills/` has an entry in `~/.agents/skills/`.
- `install-symlink`: each entry is a symlink, not a copied directory.
- `install-target`: each symlink resolves inside this checkout.

## How to get to it (user POV)

- Type a slash skill (`/how`, `/unslop`, `/poteto-mode`) in any session on claude code, codex, gemini cli, opencode, amp, pi, goose, droid, or crush. The harness offers it because the link farm exposes it.
- The README's install step creates the farm: `mkdir -p ~/.agents/skills && ln -sfn /path/to/pstack-portable/skills/* ~/.agents/skills/`.

## Driving it with pi

Preconditions:

- doctor has run this session (its install section is this feature's bulk check).
- `~/.agents/skills/` exists.

- Full install audit, expect `doctor: ok` or `FAIL` lines naming missing links: `python3 .agents/skills/verify-pstack/verify.py doctor`
- Spot-check three links resolve into the checkout, expect three paths under the repo root's `skills/` directory: `readlink -f ~/.agents/skills/how ~/.agents/skills/unslop ~/.agents/skills/poteto-mode`
- Negative check on shadowing, expect no output: for each of `how`, `unslop`, `poteto-mode`, confirm `~/.agents/skills/<name>` is a symlink (`test -L ~/.agents/skills/how && echo linked`)
- User-visible end state: the session's own skill list contains pstack skills by slash name. In the pi session running the drive, the loaded skills include `how`, `unslop`, and `poteto-mode` from this checkout. Save that observation to evidence.

## Gotchas

- A copied directory instead of a symlink loads the text but breaks every relative reference. The doctor flags it; do not "fix" it by copying again.
- A real directory at the same name shadows the repo skill. pi loads the copy, so edits in this checkout never appear. The doctor catches this as a non-symlink; the fix is replacing the copy with a link, which belongs to the user, not the verification run.
- A dangling link means the checkout moved. Report the old target; never delete the user's links without saying so.
- Verification never repairs the install. Report, hand back the fix command, and let the user or a setup run apply it.
