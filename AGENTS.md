# Repository guidance

pstack-portable is a collection of agent skills and personas. The Markdown files are the product. Keep skill instructions portable across supported harnesses; route harness-specific operations through [skills/harness/SKILL.md](skills/harness/SKILL.md) and its adapters.

- Preserve relative links between skills and their references. Installed skills may be symlinks into this checkout.
- When porting upstream changes, keep the local `pstack-tdd` and `pstack-teach` names and the harness-neutral wording. See [upstream sync](README.md#upstream-sync) for the fork's conventions.
- Before claiming a pstack change works, follow [.agents/skills/verify-pstack/SKILL.md](.agents/skills/verify-pstack/SKILL.md). It defines the static check, cold-load proof, and evidence requirements.
