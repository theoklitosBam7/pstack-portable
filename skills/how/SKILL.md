---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement, ownership, or layering questions. Explains subsystem architecture, runtime flow, and onboarding mental models. Use why for motivation."
disable-model-invocation: true
---

# How

Explore the codebase to answer "how does X work?" Produce an architectural explanation for an engineer joining the subsystem. Build a working mental model without turning the answer into annotated source code.

Resolve model roles through the **harness** skill. Use `~/.config/pstack/models` first, then the active harness adapter's defaults. Use the harness spawn operation and fallback rules for each subagent.

## Step 1. Assess complexity

If the scope is unclear, state your best interpretation and explore. Let the user redirect you.

- **Simple.** A question about one module or a small utility. Skip explorers. One explainer explores and answers in one pass. Go to Step 2b.
- **Complex.** A question about a subsystem across files or services, a cross-cutting feature, or a full architecture. Spawn parallel explorers, then ask an explainer to combine their findings. Go to Step 2a.

When in doubt, use the simple path.

## Step 2a. Explore a complex question

Split the question into two to four distinct exploration angles. For example, a rate limiter could have separate angles for its state, request path, and configuration.

Spawn all explorers in one call through the **harness** skill:

- Mode: `readonly`.
- Model role: `how explorer`.
- Prompt: use `references/explorer-prompt.md` and add the explorer's angle.

Each explorer traces its slice from an entry point through the full flow. It reads the code, names files, and reports non-obvious behavior. It does not guess from file names.

After the explorers return, go to Step 3.

## Step 2b. Explain a simple question

Spawn one readonly subagent through the **harness** skill:

- Model role: `how explainer`.
- Prompt: use `references/explainer-prompt.md` without the explorer-findings section.

Go to Step 4 when the explainer returns.

## Step 3. Synthesize complex findings

Spawn one readonly subagent through the **harness** skill:

- Model role: `how explainer`.
- Prompt: use `references/explainer-prompt.md` and include every explorer's findings.

The explainer reconciles overlaps and contradictions, then writes one coherent account. Go to Step 4 when it returns.

## Step 4. Present the explanation

Present the explainer's answer. Edit lightly for clarity or to add context from the conversation. Keep the explanation intact.

## Output format

Use the sections in `references/explainer-prompt.md` that fit the question: Overview, Key Concepts, How It Works, Where Things Live, and Gotchas.
