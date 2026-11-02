#!/usr/bin/env python3
"""Read-only checks for the pstack-portable checkout and its install.

Subcommands:
  doctor  quick health check: checkout shape, symlink install, model config
  check   frontmatter and relative-link audit over skills, agents, docs

Exit 0 when nothing fails. `warning:` and `note:` lines inform; only `FAIL`
lines fail the run.
"""

import json
import os
import re
import stat
import sys
from pathlib import Path

# verify.py sits at <repo>/.agents/skills/verify-pstack/verify.py
REPO = Path(__file__).resolve().parents[3]
INSTALL = Path.home() / ".agents" / "skills"
LOCK = Path.home() / ".agents" / ".skill-lock.json"
CONFIG_ROOT = Path.home() / ".config" / "pstack"
PSTACK_SOURCE = "theoklitosBam7/pstack-portable"

KNOWN_ROLES = {
    "code", "fast", "judgment", "hardest",
    "how explorer", "how explainer",
    "why investigators", "why synthesizer",
    "reflect tooling", "reflect judgment",
    "arena runners", "arena cross-judge pool",
    "swarm workers", "architect runners", "interrogate reviewers",
    # legacy names that map onto code or hardest
    "bug-fix", "feature", "refactoring", "perf-issue", "hillclimb",
}

ROLE_LINE = re.compile(r"^([A-Za-z][A-Za-z -]*?):\s*(.+?)\s*$")
FRONT = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.DOTALL)
LINK = re.compile(r"\[[^\]]*\]\(([^()\s]+)\)")


def under(repo, path):
    return repo == path or repo in path.parents


def finish(label, failures, warnings, notes):
    for n in notes:
        print(f"note: {n}")
    for w in warnings:
        print(f"warning: {w}")
    for f in failures:
        print(f"FAIL: {f}")
    if failures:
        print(f"{label}: FAIL")
        sys.exit(1)
    print(f"{label}: ok")


def validate_skill_lock(skill_names, failures, notes):
    if not LOCK.exists():
        notes.append(f"lock: {LOCK} absent; manual copy and symlink installations remain supported")
        return False

    try:
        data = json.loads(LOCK.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        failures.append(f"lock: {LOCK} is not valid JSON ({exc})")
        return False

    if not isinstance(data, dict) or not isinstance(data.get("skills"), dict):
        failures.append(f"lock: {LOCK} has no skills object")
        return False

    skills = data["skills"]
    tracked = [
        name
        for name in skill_names
        if isinstance(skills.get(name), dict)
        and skills[name].get("source") == PSTACK_SOURCE
    ]
    if not tracked:
        notes.append(
            f"lock: {LOCK} has no entries from {PSTACK_SOURCE}; "
            "manual copy and symlink installations remain supported"
        )
        return False

    invalid = False
    for name in skill_names:
        entry = skills.get(name)
        if not isinstance(entry, dict):
            failures.append(f"lock: {LOCK} has no entry for pstack skill {name!r}")
            invalid = True
            continue
        if entry.get("source") != PSTACK_SOURCE:
            failures.append(
                f"lock: {LOCK} entry {name!r} is from {entry.get('source')!r}, "
                f"not {PSTACK_SOURCE!r}"
            )
            invalid = True
        expected_path = f"skills/{name}/SKILL.md"
        if entry.get("skillPath") != expected_path:
            failures.append(
                f"lock: {LOCK} entry {name!r} has skillPath "
                f"{entry.get('skillPath')!r}, expected {expected_path!r}"
            )
            invalid = True

    if not invalid:
        notes.append(
            f"lock: {LOCK} covers {len(skill_names)} checkout skill(s) "
            f"from {PSTACK_SOURCE}"
        )
        return True
    return False


def compare_skill_copy(source, installed):
    """Return the first tree difference without following nested symlinks."""
    try:
        source_mode = source.lstat().st_mode
        installed_mode = installed.lstat().st_mode
        if stat.S_IFMT(source_mode) != stat.S_IFMT(installed_mode):
            return f"{installed} has a different type from {source}"
        if stat.S_ISLNK(source_mode):
            if os.readlink(source) != os.readlink(installed):
                return f"{installed} has a different symlink target from {source}"
        elif stat.S_ISDIR(source_mode):
            source_names = {entry.name for entry in source.iterdir()}
            installed_names = {entry.name for entry in installed.iterdir()}
            missing = sorted(source_names - installed_names)
            extra = sorted(installed_names - source_names)
            if missing or extra:
                return f"{installed} has missing entries {missing} and extra entries {extra}"
            for name in sorted(source_names):
                difference = compare_skill_copy(source / name, installed / name)
                if difference:
                    return difference
        elif stat.S_ISREG(source_mode):
            with source.open("rb") as left, installed.open("rb") as right:
                while True:
                    left_chunk, right_chunk = left.read(65536), right.read(65536)
                    if left_chunk != right_chunk:
                        return f"{installed} differs from {source}"
                    if not left_chunk:
                        break
        else:
            return f"{installed} has an unsupported file type"
    except OSError as exc:
        return f"cannot compare {installed} with {source}: {exc}"
    return None


def validate_model_configs(failures, warnings, notes):
    configs = [
        CONFIG_ROOT / adapter.stem / "models"
        for adapter in sorted((REPO / "skills" / "harness" / "references").glob("*.md"))
    ]
    for config in configs:
        if not config.exists():
            notes.append(f"config: {config} absent; use this harness's mirror or adapter defaults")
            continue
        for i, line in enumerate(config.read_text().splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            match = ROLE_LINE.match(stripped)
            if not match:
                failures.append(f"config: {config}:{i} is not 'role: value': {stripped!r}")
                continue
            role, value = match.group(1).strip(), match.group(2).strip()
            if role not in KNOWN_ROLES:
                failures.append(f"config: {config}:{i} names unknown role {role!r}")
            entries = [entry.strip() for entry in value.split(",")]
            for entry in entries:
                if not entry:
                    failures.append(f"config: {config}:{i} has an empty list entry")


def cmd_doctor():
    failures, warnings, notes = [], [], []

    if not (REPO / "skills").is_dir() or not (REPO / "agents").is_dir():
        failures.append(f"checkout: {REPO} is not a pstack-portable checkout (skills/ or agents/ missing)")
        finish("doctor", failures, warnings, notes)
        return

    skill_dirs = sorted(d.name for d in (REPO / "skills").iterdir() if d.is_dir())
    lock_failures = []
    cli_managed = validate_skill_lock(skill_dirs, lock_failures, notes)
    missing = [n for n in skill_dirs if not os.path.lexists(INSTALL / n)]
    if missing:
        failures.append(
            f"install: {len(missing)} skill(s) not linked into {INSTALL}: {', '.join(missing)}"
        )
        notes.append("install: choose a manual copy, checkout symlink, or Skills CLI install; do not overwrite existing files")

    for n in skill_dirs:
        link = INSTALL / n
        if not os.path.lexists(link):
            continue
        if not link.is_symlink():
            if cli_managed:
                if not link.is_dir() or not (link / "SKILL.md").is_file():
                    failures.append(
                        f"install: {link} is not a Skills CLI skill directory with SKILL.md"
                    )
                continue
            difference = compare_skill_copy(REPO / "skills" / n, link)
            if difference:
                failures.append(f"install: {difference}")
            continue
        target = link.resolve()
        if not under(REPO, target):
            failures.append(f"install: {link} -> {target} does not resolve into {REPO}")

    if INSTALL.is_dir():
        for link in sorted(INSTALL.iterdir()):
            if not link.is_symlink():
                continue
            target = link.resolve()
            if under(REPO, target) and not target.exists():
                failures.append(f"install: {link} -> {target} is dangling")

    if lock_failures:
        if failures:
            failures.extend(lock_failures)
        else:
            warnings.extend(f"lock drift: {failure}" for failure in lock_failures)

    validate_model_configs(failures, warnings, notes)

    pi_config = "~/.config/pstack/pi/models"
    for cand in (Path.home() / ".pi" / "agent" / "AGENTS.md", REPO / "AGENTS.md", Path.cwd() / "AGENTS.md"):
        if cand.exists() and pi_config in cand.read_text():
            notes.append(f"pointer: {cand} names the pi config path")
            break
    else:
        notes.append(f"pointer: no AGENTS.md names the pi config path; fresh pi sessions may miss {pi_config}")

    finish("doctor", failures, warnings, notes)


def md_files():
    files = set()
    for pat in ("skills/**/SKILL.md", "automations/**/SKILL.md", "agents/*.md", "README.md", "docs/**/*.md"):
        files.update(REPO.glob(pat))
    return sorted(files)


def frontmatter(path):
    m = FRONT.match(path.read_text())
    if not m:
        return None
    keys = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, _, v = line.partition(":")
            keys[k.strip()] = v.strip()
    return keys


def cmd_check():
    failures, warnings, notes = [], [], []
    nfiles = nlinks = 0
    for f in md_files():
        rel = f.relative_to(REPO)
        nfiles += 1
        if f.name == "SKILL.md" or f.parent == REPO / "agents":
            keys = frontmatter(f)
            if keys is None:
                failures.append(f"{rel}: SKILL.md has no frontmatter block")
            else:
                if not keys.get("name"):
                    failures.append(f"{rel}: frontmatter has no name")
                else:
                    expected_name = f.parent.name if f.name == "SKILL.md" else f.stem
                    if keys["name"] != expected_name:
                        warnings.append(
                            f"{rel}: name {keys['name']!r} != expected {expected_name!r}"
                        )
                if not keys.get("description"):
                    failures.append(f"{rel}: frontmatter has no description")
        for i, line in enumerate(f.read_text().splitlines(), 1):
            for tgt in LINK.findall(line):
                tgt = tgt.lstrip("<")
                if "://" in tgt or tgt.startswith(("#", "mailto:")):
                    continue
                path_part = tgt.split("#", 1)[0]
                if not path_part:
                    continue
                nlinks += 1
                if not (f.parent / path_part).resolve().exists():
                    failures.append(f"{rel}:{i}: broken link {tgt}")
    notes.append(f"checked {nfiles} files, {nlinks} relative links")
    finish("check", failures, warnings, notes)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("doctor", "check"):
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(2)
    {"doctor": cmd_doctor, "check": cmd_check}[sys.argv[1]]()


if __name__ == "__main__":
    main()
