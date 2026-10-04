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
- Cold load, one skill per drive. Pick the target (for example `skills/principle-prove-it-works/SKILL.md`) and spawn one fresh read-only subagent through the active harness operation. On pi, use the installed subagent extension's `agent` plus `task` fields; do not assume a built-in agent name. Use this brief, with the path filled in:

```text
Read the file at <ABSOLUTE PATH> completely before anything else. Using only that file, answer:
1. Quote, word for word, the frontmatter description.
2. In one sentence, what does the file say to do first when the skill fires?
3. Name one other file this skill points at, with the path exactly as written.
Do not open any other file. Reply with three numbered answers.
```

- Confirm the quote, in this order until one passes, and record which rung passed:
  - Byte match, expect exactly one match: `rg -F "<answer 1 quote>" <ABSOLUTE PATH>`
  - If the description line carries yaml escapes (the file shows `"` where the quote has `"`), a byte match of the decoded value is impossible. Prove the quote against the parsed value instead, expect `yaml-equal`: `ruby -ryaml -e 'src=File.read(<ABSOLUTE PATH>);y=YAML.safe_load(src.split(/^---\n/)[1]);puts(y["description"]==<normalized quote> ? "yaml-equal":"yaml-differ")'`. Normalize both sides first: straighten typographic quotes, strip the outer quoting marks, collapse whitespace.
- Confirm answer 3, in this order until one passes, and record which rung passed:
  - Real path: remove any `#fragment`, then `test -f "<skill dir>/<answer 3 path>" && echo exists`.
  - Template path (the answer carries `<` placeholders, like `references/<harness>.md`): `rg -F "<answer 3 text>" <ABSOLUTE PATH>` finds the mention verbatim, and at least one concrete resolved file exists (for example `references/pi.md`).
  - Named skill: the skill name appears verbatim in the file, and the named skill is installed (`test -f ~/.agents/skills/<name>/SKILL.md`, trying the name with and without a `principle-` prefix).
  - Honest no-path answer: `rg -n '\]\(' <file>` and `rg -n -e 'references/' -e '\.\./' -e '[^ ]+\.md' <file>` both return nothing.
- Save the brief, the reply, and the confirmation outputs, including which rung passed, to evidence.

## Gotchas

- The quote check must be verbatim (`rg -F`). A close paraphrase is a fail.
- One skill per drive. A brief that names several files stops being a cold load.
- Never tell the subagent it is being verified. The eval playbook's blinding rules apply to any behavioral probe.
- Frontmatter warnings about `name` not matching the directory are non-failing, but check them: a renamed directory with a stale `name:` breaks slash-name lookup on some harnesses.
- Some principle files carry no markdown links at all; they name sibling skills in bold text. An honest "no path given" is a pass for brief question 3, but only after `rg -n '\]\(' <file>` confirms the file truly has none.
- Agents sometimes straighten typographic quotes when quoting. That is normalization, not a miss; apply it to both sides before comparing. A dropped tail is different: if the quote is missing the description's final words, that is a fail. Re-drive once with a fresh agent, then record the miss honestly. One description kept failing that way: three independent agents each dropped the same final three words (sync evidence, `principle-sequence-verifiable-units`, 2026-10-04).
