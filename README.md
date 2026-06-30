# cskill

A **mini, token-frugal** Claude Code plugin — the good parts of heavy orchestration
frameworks (like [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode))
without the token cost.

Big frameworks burn tokens by loading many agents with large system prompts and fanning
them out in parallel. cskill keeps the useful ideas — orchestration, model routing, skill
reuse, specialized agents — but stays cheap:

- **3 lean agents**, short prompts.
- **Cheap-model routing** — the cheapest model that can do the job; escalate only when needed.
- **Single-threaded by default** — no agent fan-out unless the work genuinely warrants it.
- **Skill reuse** — solve a problem once, recall it cheaply forever.

## Install

```
/plugin marketplace add https://github.com/<you>/cskill
/plugin install cskill@cskill
```

(Or `/plugin marketplace add <local-path>` for local development.)

## Commands

| Command | What it does |
|---------|--------------|
| `/cskill:auto [task]` | Lightweight autopilot: understand → change → verify. Delegates only when the work is heavy; routes to the cheapest capable model. |
| `/cskill:skill-save [name]` | Save the pattern just solved as a reusable skill so it's never re-derived. |

## Agents

| Agent | Model | Role |
|-------|-------|------|
| `cs-explorer` | haiku | Read-only search/locate across the repo. Returns conclusions, not file dumps. |
| `cs-coder` | sonnet | Implements a well-scoped change and verifies it. |
| `cs-reviewer` | sonnet | Reviews a diff for real correctness bugs. Read-only. |

These are invoked automatically by `/cskill:auto`, or you can ask for them by name.

## Model routing policy

- **haiku** — search, location, mechanical lookups (`cs-explorer`).
- **sonnet** — code edits and review (`cs-coder`, `cs-reviewer`), and most autopilot work.
- **opus** — only for genuinely hard reasoning, and only when explicitly escalated.

## How the token savings work

1. Short prompts → less to load per agent.
2. Inline-by-default → no delegation overhead for small tasks.
3. No reflexive parallel fan-out → you don't pay N× context for one task.
4. Skills cache solutions → recurring problems stop costing a fresh derivation.

## Layout

```
.claude-plugin/
  plugin.json          # plugin manifest
  marketplace.json     # makes the repo installable
agents/                # cs-explorer, cs-coder, cs-reviewer
commands/              # auto, skill-save
skills/                # reusable patterns (populated by /cskill:skill-save)
```
