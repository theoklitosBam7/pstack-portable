# Install

A harness session can load every pstack skill by its slash name through either the official Skills CLI install or a manual symlink install. The CLI records its installed skills in `~/.agents/.skill-lock.json`; the manual path keeps one symlink per `skills/` directory, with each link resolving into this checkout.

## Sub-features

- `install-complete`: every directory under `skills/` has an entry in `~/.agents/skills/`.
- `install-symlink`: each manual-install entry is a symlink, not a copied directory.
- `install-target`: each symlink resolves inside this checkout.
- `install-lock`: the global Skills CLI lock records every checkout skill with the expected source and path.

## How to get to it (user POV)

- Type a slash skill (`/how`, `/unslop`, `/poteto-mode`) in any session on claude code, codex, gemini cli, opencode, amp, pi, goose, droid, crush, or github copilot cli. The harness offers it because the install exposes it.
- Install globally with the official Skills CLI: `npx skills@latest add theoklitosBam7/pstack-portable -g --all -y`. The CLI records the install in `~/.agents/.skill-lock.json`.
- Install manually from a stable checkout with the README's absolute-path symlink command.
- The README's install step creates the farm: `mkdir -p ~/.agents/skills && ln -sfn /path/to/pstack-portable/skills/* ~/.agents/skills/`.

## Driving it with pi

Preconditions:

- doctor has run this session (its install section is this feature's bulk check).
- `~/.agents/skills/` exists.

- Full install audit, expect `doctor: ok` or `FAIL` lines naming missing links or lock drift: `python3 .agents/skills/verify-pstack/verify.py doctor`
- Spot-check three links resolve into the checkout, expect three paths under the repo root's `skills/` directory: `readlink -f ~/.agents/skills/how ~/.agents/skills/unslop ~/.agents/skills/poteto-mode`
- Negative check on shadowing, expect no output: for each of `how`, `unslop`, `poteto-mode`, confirm `~/.agents/skills/<name>` is a symlink (`test -L ~/.agents/skills/how && echo linked`)
- User-visible end state: the session's own skill list contains pstack skills by slash name. In the pi session running the drive, the loaded skills include `how`, `unslop`, and `poteto-mode` from this checkout. Save that observation to evidence.

## Gotchas

- A copied directory without a valid Skills CLI lock is not a valid manual install. The doctor flags it; do not "fix" it by copying again.
- A Skills CLI install may use copied directories. The doctor accepts them only when `~/.agents/.skill-lock.json` records every checkout skill from `theoklitosBam7/pstack-portable` with its expected `skillPath`.
- A real directory at the same name without a valid Skills CLI lock shadows the repo skill. pi loads the copy, so edits in this checkout never appear. The doctor catches this as a non-symlink; the fix is replacing the copy with a link, which belongs to the user, not the verification run.
- A dangling link means the checkout moved. Report the old target; never delete the user's links without saying so.
- Verification never repairs the install. Report, hand back the fix command, and let the user or a setup run apply it.
