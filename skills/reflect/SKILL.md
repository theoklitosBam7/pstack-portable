---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
disable-model-invocation: true
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

## When to invoke

- The user said "reflect" or "/reflect".
- A complex task (5+ tool calls) just landed cleanly and the recipe is worth keeping.
- The agent hit dead ends, found the working path, and the path generalizes.
- The user corrected the agent's approach mid-task.
- A non-trivial workflow emerged that isn't captured anywhere.

Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## Process

### 1. Locate the active transcript

The parent finds its own transcript file before fanning out, with the find-transcripts operation in the **harness** skill. Stay inside the active workspace. Reading another project's transcripts crosses workspace boundaries and reads private chats from unrelated projects.

```bash
ls -t <transcripts-dir>/*.jsonl <transcripts-dir>/*/*.jsonl <transcripts-dir>/*/subagents/*.jsonl 2>/dev/null | head -10
```

Transcript layouts differ per harness. Handle a flat file per session, a nested directory per session, and subagent transcripts inside their parent's. The harness adapter names the shapes it uses.

For each candidate, read the first JSONL line and check that `message.content[0].text` contains the conversation's opening user prompt. Take the matching path. If no path resolves, write a tight digest of the session and pass that instead.

### 2. Spawn three reviewers in parallel

One message, three subagents with explicit model roles from the pstack model config, per the **harness** skill, in agent mode. Reviewers need MCP access for context lookups, tickets, chat threads, observability traces referenced in the transcript, where the harness strips MCPs in readonly mode. The prompt forbids file writes; the parent applies edits.

| Lens | Model role | Prompt template |
|---|---|---|
| Judgment | the `reflect judgment` role from the pstack model config, adapter default otherwise | `references/judgment-reviewer.md` |
| Tooling | the `reflect tooling` role from the pstack model config, adapter default otherwise | `references/tooling-reviewer.md` |
| Divergent | the `reflect judgment` role from the pstack model config, adapter default otherwise | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in their response.

### 3. Synthesize

One subagent, using the `reflect judgment` role from the pstack model config, adapter default otherwise, in agent mode per the **harness** skill. The synthesizer's quality check includes spot-verifying citations, which can require MCP access. Use `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. The synthesizer returns a structured Accepted / Rejected / Backlog list.

### 4. Structural enforcement check

Sanity-check the synthesizer's Accepted list. For any item that would be enforced more reliably by a lint rule, script, metadata flag, or runtime check, move it from Accepted to Backlog. The synthesizer already applies this criterion; this is a final pass before edits land. See the **encode-lessons-in-structure** principle skill.

### 5. Apply

Before applying any Accepted edit, present the synthesizer's full Accepted/Rejected/Backlog output to the user and wait for explicit approval. The user picks which subset to apply and may redirect routings. Skill changes affect every future agent in the org; do not auto-apply.

Backlog items file to whatever devex / backlog tracker your team uses automatically. Those are tracker submissions, not skill edits. Only the Accepted list waits for approval.

For each approved Accepted item, follow the Routing field exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): parent does directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the harness's skill-authoring helper when it has one, Cursor's `/create-skill`, and run its draft / test / iterate loop. Otherwise apply the edit directly.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): use the helper's description-optimization loop where one exists, otherwise tune the description yourself against the trigger phrases that missed.
- `new skill via <kebab-name>`: hand creation to the helper where one exists. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done. Skip this step if it doesn't.

### 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
