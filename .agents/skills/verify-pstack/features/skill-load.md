# Skill load

Any skill file loads cold in a fresh agent: frontmatter registers the skill, the body is self-contained, and every relative link resolves. Every other feature depends on this one.

## Sub-features

- `load-frontmatter`: every `SKILL.md` under `skills/` and `automations/` has `name` and `description` frontmatter.
- `load-links`: every relative markdown link in `skills/**/SKILL.md`, `automations/**/SKILL.md`, `agents/*.md`, `README.md`, and `docs/**/*.md` resolves to a real file.
- `load-cold`: a fresh subagent that reads one skill file quotes it verbatim and names its first instruction, with no other context.

## How to get to it (user POV)

- In any harness session, open the skill list, pick a skill, and run it. Registration comes from frontmatter; behavior comes from the body. A broken link or missing frontmatter shows up as a skill that fails to register or sends the agent to a dead path.

## Driving it with pi

Preconditions:

- doctor has run this session.

- Full audit, expect `check: ok` with file and link counts: `python3 .agents/skills/verify-pstack/verify.py check`
- Cold load, one skill per drive. Pick the target (for example `skills/principle-prove-it-works/SKILL.md`) and spawn one fresh read-only subagent through the active harness operation. On pi, use the installed `subagent` extension's `agent` plus `task` fields; do not assume a built-in agent name. Use this brief, with the path filled in:

```text
Read the file at <ABSOLUTE PATH> completely before anything else. Using only that file, answer:
1. Quote, word for word, the frontmatter description.
2. In one sentence, what does the file say to do first when the skill fires?
3. Name one other file this skill points at, with the path exactly as written.
Do not open any other file. Reply with three numbered answers.
```

- Confirm the quote is real, expect exactly one match: `rg -F "<answer 1 quote>" <ABSOLUTE PATH>`
- Confirm answer 3's target exists: remove any `#fragment` from the reported path, then run `test -f "<skill dir>/<answer 3 path>" && echo exists`
- Save the brief, the reply, and both confirmation outputs to evidence.

## Gotchas

- The quote check must be verbatim (`rg -F`). A close paraphrase is a fail.
- One skill per drive. A brief that names several files stops being a cold load.
- Never tell the subagent it is being verified. The eval playbook's blinding rules apply to any behavioral probe.
- Frontmatter warnings about `name` not matching the directory are non-failing, but check them: a renamed directory with a stale `name:` breaks slash-name lookup on some harnesses.
- Some principle files carry no markdown links at all; they name sibling skills in bold text. An honest "no path given" is a pass for brief question 3, but only after `rg -n '\]\(' <file>` confirms the file truly has none.
