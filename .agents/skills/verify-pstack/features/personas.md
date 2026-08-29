# Personas

Two markdown subagent personas ship in `agents/`: `poteto-agent.md` (runs poteto-mode end to end) and `comment-sicko.md` (read-only comment reviewer). Harnesses with persona support install them into their persona directory; others inline the file's text at the top of the brief.

## Sub-features

- `persona-files`: both files exist with `name` and `description` frontmatter.
- `persona-links`: the README and skill links to `agents/*.md` resolve.
- `persona-install`: where installed (pi: `~/.pi/agent/agents/`), the copy matches the checkout byte for byte.

## How to get to it (user POV)

- On cursor, spawn `subagent_type: "poteto-agent"` from a parent agent.
- On every other harness, the `harness` skill's persona operation installs `agents/*.md` into the persona directory, for example `~/.pi/agent/agents/` on pi, or inlines the file into the brief.

## Driving it with pi

Preconditions:

- doctor has run this session (the checker's `agents/*.md` frontmatter audit is the source-side bulk check).

- Frontmatter and link audit, expect `check: ok` (it covers `agents/*.md`): `python3 .agents/skills/verify-pstack/verify.py check`
- Install drift check. If `~/.pi/agent/agents/poteto-agent.md` exists, expect no output: `diff ~/.pi/agent/agents/poteto-agent.md agents/poteto-agent.md` (same for `comment-sicko.md`).
- If the persona directory does not exist, record `verified-unreachable: persona not installed; inline path is the live route` and prove the inline route instead: the cold load of a skill in `skill-load.md` shows the body a brief would inline is complete.

## Gotchas

- An installed persona copied long ago drifts silently from the checkout. diff, never assume.
- Do not install or overwrite a persona from a verification run. That mutates the user's harness config, and repair belongs to a setup action.
- The inline route means persona absence does not break poteto-mode. Treat a missing install as a finding, not a failure of the skill.
