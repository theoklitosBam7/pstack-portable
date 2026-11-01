# The pstack guide

pstack works best when you stop micromanaging the agent. You describe what you want and how you'll know it's done. `/poteto-mode` picks the playbook, runs the other skills as the steps need them, and shows you the evidence. This guide teaches that habit with realistic prompts.

Here's what you'll learn:

1. [Set up pstack](./01-setup.md). Install pstack and pick your models.
2. [Route work through `/poteto-mode`](./02-poteto-mode.md). Give it a goal and watch it pick a playbook.
3. [Understand the code](./03-understand.md). `/how`, `/why`, `/pstack-teach`, and `/recall` before you edit anything.
4. [Design the change](./04-design.md). Explore designs with `/architect`, `/arena`, `/swarm`, and `/interrogate`, then use prototypes and plans.
5. [Build and clean the change](./05-build-and-clean.md). The build playbooks, `/pstack-tdd`, `/unslop`, and `/no-comments`.
6. [Verify and ship](./06-verify-and-ship.md). Check app behavior, verify properties, vet benchmarks, and ship a focused PR.
7. [Run work while you sleep](./07-overnight.md). Establish trust before loops, keep a decision log, and coordinate work across agents.
8. [Steer with principle names](./08-principles.md). The 24 names that redirect an agent mid-task.
9. [Make it yours](./09-make-it-yours.md). Make your own mode, use `/correct` for repeated mistakes, and test skill changes.
10. [Recipes and pitfalls](./10-recipes-and-pitfalls.md). Prompts to copy and mistakes to skip.

Read the pages in order the first time. After that, each page stands alone.

## If you only remember one thing

Give the agent a goal and a way to check it, in your own words:

```text
/poteto-mode the export writes duplicate rows when a retry lands mid-run. repro first, then fix and verify.
```

You don't need to name a playbook or list skills. "repro first" and a checkable outcome are all the routing signal `/poteto-mode` needs. It matches the Bug fix playbook, copies the steps into a todo list, and calls the right skills as each step fires.

Next: [Set up pstack](./01-setup.md).
