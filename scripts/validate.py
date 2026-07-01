#!/usr/bin/env python3
"""Validate the cskill plugin structure.

A lightweight, dependency-free regression check: parse the frontmatter of every
agent, command, and skill, and confirm the plugin's contracts still hold — valid
model names, referenced agents that actually exist, names that match filenames,
and manifests that parse. Run it before committing a change to agents/, commands/,
or skills/.

Usage:  python3 scripts/validate.py
Exit:   0 = all checks pass, 1 = at least one error.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Models cskill routes to. Bare tier names are what the plugin uses today; full
# API ids are accepted too so a future pin (e.g. claude-haiku-4-5-...) won't trip.
KNOWN_MODEL_TIERS = {"haiku", "sonnet", "opus"}
SKILL_INDEX_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|", re.MULTILINE)

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def parse_frontmatter(path: Path) -> dict[str, str] | None:
    """Parse a minimal YAML frontmatter block (flat `key: value` pairs).

    Returns None if the file has no frontmatter. Values are kept as raw strings;
    this is enough for the fields cskill uses and avoids a PyYAML dependency.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    if lines[0].strip() != "---":
        return None
    fm: dict[str, str] = {}
    for i in range(1, len(lines)):
        line = lines[i]
        if line.strip() == "---":
            return fm
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip()
    # No closing delimiter found.
    err(f"{rel(path)}: frontmatter opened with '---' but never closed")
    return fm


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def model_ok(value: str) -> bool:
    v = value.strip().strip("'\"")
    return v in KNOWN_MODEL_TIERS or v.startswith("claude-")


def check_agents() -> set[str]:
    """Validate agents/*.md; return the set of defined agent names."""
    names: set[str] = set()
    agents_dir = ROOT / "agents"
    if not agents_dir.is_dir():
        err("agents/ directory is missing")
        return names
    for path in sorted(agents_dir.glob("*.md")):
        fm = parse_frontmatter(path)
        if fm is None:
            err(f"{rel(path)}: no frontmatter")
            continue
        for field in ("name", "description", "tools", "model"):
            if field not in fm:
                err(f"{rel(path)}: missing required field '{field}'")
        name = fm.get("name", "")
        if name:
            names.add(name)
            if name != path.stem:
                err(f"{rel(path)}: name '{name}' != filename '{path.stem}'")
        if "model" in fm and not model_ok(fm["model"]):
            err(f"{rel(path)}: unknown model '{fm['model']}'")
    return names


def check_commands(agent_names: set[str]) -> None:
    commands_dir = ROOT / "commands"
    if not commands_dir.is_dir():
        err("commands/ directory is missing")
        return
    for path in sorted(commands_dir.glob("*.md")):
        fm = parse_frontmatter(path)
        if fm is None:
            err(f"{rel(path)}: no frontmatter")
            continue
        if "description" not in fm:
            err(f"{rel(path)}: missing required field 'description'")
        if "model" in fm and not model_ok(fm["model"]):
            err(f"{rel(path)}: unknown model '{fm['model']}'")
        agent = fm.get("agent")
        if agent and agent not in agent_names:
            err(f"{rel(path)}: references agent '{agent}' which is not defined in agents/")
        # A forked command that names an agent should keep the command model in
        # sync with that agent's model (they load together); flag a mismatch.
        if fm.get("context") == "fork" and agent and "model" in fm:
            agent_fm = parse_frontmatter(ROOT / "agents" / f"{agent}.md") or {}
            if agent_fm.get("model") and agent_fm["model"] != fm["model"]:
                warn(
                    f"{rel(path)}: model '{fm['model']}' differs from agent "
                    f"'{agent}' model '{agent_fm['model']}'"
                )


def check_skills() -> None:
    skills_dir = ROOT / "skills"
    if not skills_dir.is_dir():
        err("skills/ directory is missing")
        return
    index_path = skills_dir / "README.md"
    if not index_path.is_file():
        err("skills/README.md is missing")
        indexed_skills: set[str] = set()
    else:
        indexed_skills = set(SKILL_INDEX_RE.findall(index_path.read_text(encoding="utf-8")))
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        if skill_dir.name not in indexed_skills:
            err(f"skills/{skill_dir.name}/ is not listed in skills/README.md index")
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            err(f"skills/{skill_dir.name}/: missing SKILL.md")
            continue
        fm = parse_frontmatter(skill_file)
        if fm is None:
            err(f"{rel(skill_file)}: no frontmatter")
            continue
        for field in ("name", "description"):
            if field not in fm:
                err(f"{rel(skill_file)}: missing required field '{field}'")
        name = fm.get("name", "")
        if name and name != skill_dir.name:
            err(f"{rel(skill_file)}: name '{name}' != directory '{skill_dir.name}'")


def check_manifests() -> None:
    for name in ("plugin.json", "marketplace.json"):
        path = ROOT / ".claude-plugin" / name
        if not path.is_file():
            err(f".claude-plugin/{name} is missing")
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f"{rel(path)}: invalid JSON — {e}")


def main() -> int:
    agent_names = check_agents()
    check_commands(agent_names)
    check_skills()
    check_manifests()

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s) — FAIL")
        return 1
    print(f"OK — {len(agent_names)} agents, all checks pass"
          + (f" ({len(warnings)} warning(s))" if warnings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
