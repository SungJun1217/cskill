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
/plugin marketplace add https://github.com/SungJun1217/cskill
/plugin install cskill@cskill
```

(Or `/plugin marketplace add <local-path>` for local development.)

## Commands

| Command | What it does |
|---------|--------------|
| `/cskill:auto [task]` | Lightweight autopilot: understand → change → verify. Delegates only when the work is heavy; routes to the cheapest capable model. |
| `/cskill:explore [q]` | Run the `cs-explorer` agent (haiku) directly — locate code / answer a where-how question. |
| `/cskill:plan [task]` | Run the `cs-planner` agent (opus) directly — produce a complete, unambiguous plan that ends by telling the executor to *spawn* `cs-coder` to implement and `cs-reviewer` to review (each subagent loads its own system prompt + model; it's not a model switch). |
| `/cskill:code [change]` | Run the `cs-coder` agent (sonnet) directly — implement a scoped change and verify it. |
| `/cskill:review [target]` | Run the `cs-reviewer` agent (haiku) directly — review a diff for real bugs (defaults to the working diff). |
| `/cskill:skill-save [name]` | Save the pattern just solved as a reusable skill so it's never re-derived. |

`/cskill:auto` orchestrates the agents for you; the four agent commands above are thin
direct entry points (`context: fork` → the agent) for when you already know which one you want.

## Agents

| Agent | Model | Role |
|-------|-------|------|
| `cs-explorer` | haiku | Read-only search/locate across the repo. Returns conclusions, not file dumps. |
| `cs-planner` | opus | Read-only. Turns a non-trivial task into a concrete, ordered plan. |
| `cs-coder` | sonnet | Implements a well-scoped change and verifies it. |
| `cs-reviewer` | haiku | Reviews a diff for real correctness bugs. Read-only. |

These are invoked automatically by `/cskill:auto`, or you can ask for them by name.

## Model routing policy

- **haiku** — search/location (`cs-explorer`) and diff review (`cs-reviewer`). Dry-run showed haiku catches real regressions and avoids false positives when given the intended behavior.
- **sonnet** — code edits (`cs-coder`) and most autopilot work.
- **opus** — planning a non-trivial task (`cs-planner`), and any other genuinely hard reasoning. Used deliberately, not by default — most tasks never invoke it.

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
