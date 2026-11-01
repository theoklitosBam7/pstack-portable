# Recipes and pitfalls

Prompts worth copying, then the mistakes everyone makes once. Swap in your own paths and finish conditions. The recipes are deliberately informal. That's how they get typed in practice, and the skills read intent fine.

![She tastes a finished dish while robots cook from a recipe box, with pinned cards reading /how, /pstack-tdd, and /loop above the counter.](./images/recipes.jpg)

## Understand an unfamiliar subsystem

```text
use /how first to understand how this initialization works. then use /why to figure out why it broke recently.
```

Mechanics first, history second. Each skill's report tells you which sources it searched, so you know what the answer is grounded in.

## Restate a noisy report before touching code

```text
/in-your-own-words read this thread and restate the underlying issue. don't change any code yet.
```

A restatement lets you correct a misreading before the agent changes code. Keep your own theory until the agent has stated its own.

## Sharpen a prompt before you send it

```text
/sharpen write the onboarding doc for the new billing service.
```

[`/sharpen`](../../skills/sharpen/SKILL.md) identifies what an expert would do, the material and tools they would use, and how to check the result. It rewrites your prompt without doing the task.

## Prototype before you pick

```text
/poteto-mode prototype a few options for the settings layout. put them behind a switcher and send me screenshots of each.
```

Compare working options before choosing a design. The [design guide](./04-design.md) describes the prototype workflow.

## Turn a settled design into a plan

```text
/poteto-mode turn this design into a plan. small verifiable PRs, each with its own proof.
```

The plan names the steps, their evidence, and the playbook that will execute them.

## Get a second opinion on a design

```text
ask /arena for a second opinion on this thread and our approach
```

Your current design becomes one candidate among several, and the synthesis tells you whether the panel found something better or confirmed what you had. Cheap insurance before a costly commitment.

## Check independent slices in parallel

```text
/swarm check every package under packages/ against its check.sh. one worker per package. one report.
```

Each worker owns one package. The parent waits for every slice and returns one `PASS`, `ISSUES`, or `BLOCKED` report instead of raw worker dumps.

## Review a branch skeptically

```text
/interrogate the whole branch, but skeptically. don't change anything yet. no nitpicks unless it's an actual bug or regression in behavior.
```

The qualifiers do real work. "don't change anything yet" keeps it read-only, and the nitpick rule pre-filters the noise so `Act on` findings are worth your time.

## Fix a bug through a failing test

```text
/poteto-mode repro the duplicate write first. if there's a cheap test path, /pstack-tdd it. then fix and rerun.
```

"if there's a cheap test path" matters. Forcing a test through brittle mocks proves less than running the real command, and the playbook is allowed to say so.

## Prove a property tests rarely reach

```text
/create-formal-verification-skill the retry queue. a message must never be delivered twice.
```

The result states the scope of the check, gives a counterexample if the property fails, and provides a project skill for later changes to the code.

## Vet a number before you post it

```text
/benchmark-checklist vet this 40% speedup before it goes in the pr description
```

The result states whether the change is faster, slower, indistinguishable, or inconclusive, with evidence and limits.

## Stop correcting the same mistake

```text
/correct agents keep adding new config flags without registering them in the schema
```

The skill looks for a change to the repo that prevents the mistake in later runs.

## Keep a run honest while you're away

```text
im going to bed, keep going autonomously until every fixture passes. do not stop. keep a decision log i can audit in the morning.
```

The full contract is on the [overnight page](./07-overnight.md). The short form works once the task and finish condition are already in the conversation.

## Redirect a drifting run

Steering prompts are one line:

```text
i said the goal is to repro. i did not ask for a fix yet.
```

```text
apply prove it works. show me the real output, not the build log.
```

```text
/unslop that, no emdashes
```

You rarely need more words. You need the right name, and [the principles page](./08-principles.md) is the vocabulary.

## Get the reply in plain words

```text
/bro
```

That's the whole prompt. [`/bro`](../../skills/bro/SKILL.md) restates the last message like one human talking to another, no jargon, shorter. Use it when a reply is technically thorough and you still don't know what it said.

## Catch up on a chat you left running

```text
/ketchup
```

[`/ketchup`](../../skills/ketchup/SKILL.md) reports what changed since your last message and lists decisions waiting on you with evidence and risks. It does not change the work.

[`/ketchup-video`](../../skills/ketchup-video/SKILL.md) presents the catch-up as a short subtitled video and lists the decisions as text.

## The pitfalls

- **Enumerating skills in the prompt.** "use /how then /architect then /arena" reorders steps the playbook already sequences. State the goal and constraints. Name a skill only to override a default.
- **A vague finish condition.** "make it better" gives `/loop` nothing to check. Give a command or artifact that can pass or fail.
- **Parallel agents in one worktree.** They overwrite each other and the diff becomes archaeology. Say "own worktree per attempt" and the isolation is free.
- **Using `/arena` for coverage.** `/arena` repeats one design or code brief, then picks a base and grafts the best parts. `/swarm` partitions slices or declared race arms and aggregates one report.
- **Accepting every review comment.** Bots and humans both file real catches and noise in one list. `/interrogate` sorts findings into act-on and dismissed buckets with reasons, and you can override either way.
- **Treating `auto` as a model slug.** `auto` and `inherit-parent` mean "omit the model field so the subagent inherits the parent chat model." [Setup](./01-setup.md) covers the roles.
- **Reporting success off a green build.** A build proves it compiles. Ask for the real command, flow, stored value, or profile, and expect the evidence in the reply.
- **Writing a `SKILL.md` freehand.** Route it through the [Authoring or modifying a skill playbook](../../skills/poteto-mode/playbooks/authoring-a-skill.md) so validation and review happen.

That's the guide. If you skipped ahead, go back to [setup](./01-setup.md) and run one real task. The habits stick from use, not from reading.

Back to the [guide index](./README.md).
