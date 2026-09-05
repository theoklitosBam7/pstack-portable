# Forge resolution

Use this reference whenever a playbook touches a pull request. Resolve the forge once, before the first PR operation, and keep that choice for every later operation.

- GitHub CLI (`gh`) is the default.
- If `command -v origin` succeeds and Origin can resolve the repository, use `origin pr ...` for the PR operations the playbook lists.
- If Origin is absent or cannot resolve the repository, stay on `gh` and record the fallback.
- Never require Graphite (`gt`).
- The Origin CLI is a separate `origin` executable, not the Git remote named `origin`.

Each playbook says which operations it runs through the forge (create, edit, view, watch, checks, threads, merge). Resolve before the first one, and never switch mid-playbook.
