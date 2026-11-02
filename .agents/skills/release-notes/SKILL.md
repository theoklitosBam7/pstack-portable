---
name: release-notes
description: Write or update pstack-portable GitHub release notes. Use when asked to prepare release notes or revise an existing release's notes.
---

# Release notes

Write notes for the requested pstack-portable release. Do not create a tag, create or publish a release, change release metadata, or edit an existing release unless the user asks for that action.

## Gather evidence

1. Identify the repository and target version. If the target is unclear, ask the user. For an existing GitHub release, read its current notes and metadata with `gh release view`.
2. Find the preceding relevant release and read its notes for the current style. Check the actual changes between the two release tags, including merged PRs and their authors. For an unreleased target, establish the requested endpoint before comparing. If the comparison or release boundaries are unclear, ask instead of guessing.
3. Read the changed files or PRs as needed to explain user-visible behavior, removals, migration steps, and limitations. Do not infer successful testing from a commit or PR title.

## Write

Follow the preceding release's structure unless the user requests another style. The current format is a short introduction, `## What's changed` with concise bullets, `## Pull requests` with verified titles, authors, and URLs, and a **Full changelog** link to the actual tag comparison. Explain what changed and why it matters. State any action users must take and any removed support. Use only verified links and facts; do not invent issues, PRs, features, or test results.

## Finish

If asked only to draft, show the notes without changing GitHub. If asked to update an existing release, use `gh release edit` to change its notes only. Read the release back and confirm the notes and URL. Report any missing evidence or failed command rather than claiming completion.
