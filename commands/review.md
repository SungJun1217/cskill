---
description: Review a change for real correctness bugs. Runs as the cs-reviewer agent (haiku), read-only. Defaults to the current uncommitted diff when no target is given.
argument-hint: [optional: what/where to review]
context: fork
agent: cs-reviewer
model: haiku
---

Review for real bugs. If a target is named below, review that; otherwise review the current uncommitted changes — run `git diff` and `git diff --staged` to see them, and `git status` for the changed files.

$ARGUMENTS
