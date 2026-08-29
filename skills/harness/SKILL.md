---
name: harness
description: Detect which agent harness you are running in and translate pstack's neutral operations into that harness's tools and paths. Read before any pstack skill that spawns subagents, asks a structured question, routes models, or reads transcripts. Use for /harness, "which agents does pstack run on", or setting pstack up on a new harness.
---

# Harness

pstack skills are written against a small set of neutral operations. They do not name tools or paths. This skill maps the operations onto the harness you are in right now. Every other pstack skill defers here.

## Detect once per session

Run this before the first pstack operation, then keep the answer for the session. Do not re-detect per skill.

1. Environment variables first. `CLAUDECODE=1` means Claude Code. `OPENCODE=1` or `OPENCODE_PID` set means opencode. `AI_AGENT=pi` or `PI_CODING_AGENT=true` means pi. `CODEX_SANDBOX` set means Codex CLI, a weak signal because it only appears under sandboxing.
2. Tool fingerprints next. `AskUserQuestion` plus an `Agent` tool means Claude Code. `request_user_input` plus `update_plan` means Codex CLI. `ask_user` plus `write_todos` means Gemini CLI. A `task` tool with `subagent_type` plus `todowrite` means opencode. `AskUser` plus `TaskOutput` means Factory Droid. `delegate` plus `load` means Goose. A read-only `agent` tool plus `crush_info` means Crush. Built-in specialists named `Review`, `Search`, or `Oracle` with no markdown persona support means Amp. `AskQuestion` plus a `Task` tool means Cursor.
3. Still unknown after both checks: ask the user once which harness this is, then remember it.

After detection, read `references/<harness>.md` from this skill and apply it for the rest of the session.

## Neutral operations

- **ask-user(question, options).** One structured question, two to five options, free-form always allowed. Use it where a pstack skill says to ask with options.
- **todolist(items).** A tracked task list the user can see. Update it as steps complete.
- **spawn-subagent(brief, model-role, mode).** One subagent with a standalone brief. Mode is `foreground`, `background`, or `readonly`. Fan-outs spawn all subagents in one message. The model-role names a line from the model config below, or `session` for the current model. Briefs stand alone and include goal, scope, verification, and report format.
- **persona(name).** pstack ships two personas, `poteto-agent` and `comment-sicko`, as markdown files in the plugin's `agents/` directory. When the harness supports custom subagent personas, install or reference them there. Otherwise paste the persona file's full text at the top of the subagent brief.
- **discover-mcps.** List the MCP servers configured in this harness, so a skill can pick evidence sources.
- **find-transcripts.** Locate this workspace's session transcripts on disk.
- **cloud-run(brief).** Run a subagent on managed remote compute instead of this machine. Used when a skill calls for parallel isolated workers that do not need local state.

## Model roles

Skills name roles, never model ids. Roles resolve in this order:

1. `~/.config/pstack/models`, the portable config written by `/setup-pstack`. One line per role, `role: model` or a comma-separated panel list.
2. The harness mirror named in the adapter. Cursor mirrors to `~/.cursor/rules/pstack-models.mdc` so the choices inject every session.
3. The adapter's defaults.

A role that resolves to nothing runs on the session model. The value `inherit-parent` or `auto` also means the session model. When a multi-model panel collapses to one model because the harness cannot spawn per-subagent models, say so in the reply. The panel still runs, sequentially if it must.

Roles in use: `code`, `fast`, `judgment`, `hardest`, plus the panel roles `how critics`, `how explorer`, `how explainer`, `why investigators`, `why synthesizer`, `reflect tooling`, `reflect judgment`, `arena runners`, `arena cross-judge pool`, `swarm workers`, `architect runners`, `interrogate reviewers`. Legacy config lines naming playbooks, like `bug-fix` or `feature, refactoring`, map onto `code` or `hardest` as the adapter notes.

## Fallback policy

A missing capability never skips a step. Substitute the fallback and note it in the reply.

- No subagents: do the work in the main thread, sequentially, and keep raw outputs out of the context window where the skill said to.
- No per-subagent models: the session model plays every role. Panels become sequential passes with the same briefs.
- No structured ask-user: ask in plain text and list the options as a markdown list.
- No todo tool: keep a markdown checklist in the reply and update it in place.
- No MCP discovery: name which evidence sources you could not query and proceed with the rest.
- No transcripts: state the limit, then rebuild context from git history and the shared record.
- No cloud runs: use local git worktrees plus background subagents.

## Installing pstack on a harness

Cursor installs the plugin as usual with `/add-plugin pstack`. Every other harness in the adapters reads skills from `.agents/skills/` or `~/.agents/skills/` or both, so one copy covers them: clone or place this repository, then symlink each skill into the shared directory, from the repo root:

```bash
mkdir -p ~/.agents/skills && ln -sfn "$PWD"/skills/* ~/.agents/skills/
```

If `ln` fails with `Operation not permitted`, the shared directory already holds a real directory of that name from another skills provider. `ln` replaces symlinks but never directories, so move or remove that copy first.

The `$PWD` prefix matters: `ln` stores the source text verbatim as the link's target, so a relative source such as plain `skills/*` resolves against the link's own directory, not yours, and ends up dangling. Only absolute operands produce working symlinks.

Keep the checkout intact. Skills reference their own files and sibling skills by relative path, so the symlinks must point into this tree rather than copying files out of it. `AGENTS.md` at the repo root of the target project is the always-on surface on every non-Cursor harness; add a line there naming pstack when you want its conventions applied every session.
