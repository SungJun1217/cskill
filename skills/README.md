# skills/

Reusable patterns captured by `/cskill:skill-save`. Each skill is its own folder:

```
skills/
  <slug>/
    SKILL.md   # frontmatter (name, description) + Problem / Solution / Notes
```

Claude Code auto-surfaces a skill when a new task matches its `description`, so a problem
solved once isn't re-derived — that's where cskill's token savings compound over time.

Write the `description` with the *symptoms* that should trigger recall, including concrete
keywords. Keep each skill to ~20 lines: a cheat sheet, not documentation.

## Index

Recall is automatic (by `description`); this index is for humans skimming what's here.
`scripts/validate.py` fails if a skill folder is missing from this list, so keep it current.

| Skill | Solves |
|-------|--------|
| `inclusive-date-range-off-by-one` | Date-window filter excludes the boundary day (`<` vs `<=`). |
| `run-plain-assert-tests-without-pytest` | Run `test_*.py` assert functions when pytest isn't installed. |
| `shell-injection-via-string-interpolation` | Untrusted input interpolated into a shell/SQL command string. |
