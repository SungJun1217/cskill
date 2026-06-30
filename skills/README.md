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
