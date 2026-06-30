---
description: Save the pattern/solution from the current session as a reusable cskill skill, so the next time this problem appears it isn't re-derived from scratch.
argument-hint: [optional short name]
allowed-tools: Read, Write, Bash, Grep, Glob
---

Capture what was just solved as a durable skill under `skills/`. This is how cskill saves tokens over time — solved once, recalled cheaply.

## Steps

1. Look back over the recent work in this session and identify the **one reusable pattern** worth keeping: a fix, a workflow, a gotcha, or a recipe that's likely to recur. If `$ARGUMENTS` is given, use it as the skill's short name/topic.
2. Pick a kebab-case slug (e.g. `fix-flaky-vitest-timeout`). Keep it specific.
3. Write `skills/<slug>/SKILL.md` with this exact frontmatter and structure:

```markdown
---
name: <slug>
description: <one line — the problem this solves AND the symptoms that should trigger recall, so it auto-surfaces next time. Include concrete keywords.>
---

## Problem
<1-3 sentences: what situation this applies to.>

## Solution
<The minimal steps or code that resolve it. Concrete, copy-pasteable where possible. Reference files as path:line if repo-specific.>

## Notes
<Optional: pitfalls, why the obvious approach fails, when NOT to use this.>
```

4. Keep it tight — a skill is a cheat sheet, not documentation. If it can't be stated in ~20 lines, it's probably two skills or none.
5. Confirm the file path you wrote and give a one-line summary of what was captured.

Do not save something the repo already documents, or a one-off that won't recur. If nothing is genuinely reusable, say so and don't create a file.
