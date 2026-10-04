# poteto-mode routing

`/poteto-mode` is the entry skill: it reads a task, matches one of the playbooks under `skills/poteto-mode/playbooks/`, and routes to the other skills as steps fire. Routing works only while the playbook links in its body and the README resolve.

## Sub-features

- `routing-links`: every playbook link in `skills/poteto-mode/SKILL.md` resolves to a file under `skills/poteto-mode/playbooks/`.
- `routing-index`: the inline principles index points at real principle skills.
- `routing-match`: a cold agent given a small task names the playbook the body would pick, by exact filename.

## How to get to it (user POV)

- Type `/poteto-mode <task>` at the start of any non-trivial task. The skill matches a playbook and copies the steps in verbatim.

## Driving it with pi

Preconditions:

- doctor has run this session.

- Link audit across the repo, expect `check: ok` (it includes poteto-mode): `python3 .agents/skills/verify-pstack/verify.py check`
- Playbook references are inline code, not markdown links, so the checker cannot see them. List them and test each, expect no `MISSING` lines: `rg -o 'playbooks/[a-z0-9-]+\.md' skills/poteto-mode/SKILL.md | sort -u | while read -r p; do test -f "skills/poteto-mode/$p" && echo "ok $p" || echo "MISSING $p"; done`
- Principles index: the skill names principles in bold text, some with the `principle-` prefix and some without. Resolve each, expect no `MISSING` lines: `rg -o '\*\*([a-z][a-z-]+)\*\*' skills/poteto-mode/SKILL.md -or '$1' | sort -u | while read -r n; do test -d "skills/$n" && echo "ok $n" || { test -d "skills/principle-$n" && echo "ok principle-$n" || echo "MISSING $n"; }; done`
- Cold match drive: spawn one subagent through the harness skill's spawn-subagent operation; on pi use the installed subagent extension's `agent` plus `task` fields. Use this brief:

```text
Read the file at <ABSOLUTE PATH> completely. Then read only the one playbook file it sends you to. A user gives the skill this task: "add json output to this command. text output stays byte-identical, the json parses." Which playbook did the skill's own matching rules pick? Answer with the playbook filename, then the one line in the body that justified it, quoted.
```

- Fill `<ABSOLUTE PATH>` in the brief with the checkout's absolute path to `skills/poteto-mode/SKILL.md`, then spawn.
- Confirm the named file exists: `test -f skills/poteto-mode/playbooks/<answer>.md && echo exists`
- Save the brief, the reply, and the confirmation to evidence.

## Gotchas

- Grade from the file the subagent actually opened, never from its self-report. That is the eval playbook's transcript rule.
- Do not batch several tasks into one brief. Matching is per task.
- The playbook list changes. Count the links fresh each run instead of asserting a fixed number of playbooks.
