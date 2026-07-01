# Changelog

All notable changes to cskill are documented here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); versions track `plugin.json`.

## [Unreleased]

### Added
- `scripts/validate.py` — dependency-free structure check for agents, commands,
  skills, and manifests (valid models, referenced agents exist, names match
  filenames, every skill listed in the `skills/README.md` index). Run it before
  committing changes under `agents/`, `commands/`, or `skills/`.
- This `CHANGELOG.md`.
- Skill index in `skills/README.md` (kept honest by the validator).
- Two skills seeded from a use-case test run: `run-plain-assert-tests-without-pytest`
  and `shell-injection-via-string-interpolation`.

### Changed
- `cs-explorer` gains a scope-boundary rule: locate/explain only; do not judge
  correctness or claim bugs (that's `cs-reviewer`) — flag anything incidental as
  an explicitly unverified aside. Fixes a case where the explorer confidently
  asserted a wrong bug/test-status claim that would mislead a downstream agent.

### Fixed
- README doc drift: agent count (3 → 4) and the Layout section, which omitted
  `cs-planner` and the `explore`/`plan`/`code`/`review` commands.

## [0.2.1]

### Added
- Post-plan handoff: `cs-planner` ends every plan by directing the executor to
  *spawn* `cs-coder` and `cs-reviewer` (loading their own prompts + models),
  rather than continuing as itself.

## [0.2.0]

### Added
- Opt-in per-task shared scratchpad (`.claude/run/notes.md`, gitignored) so
  spawned agents hand off findings, plans, and intended behavior across a
  fresh-context boundary.
- Direct agent commands: `/cskill:explore`, `/cskill:plan`, `/cskill:code`,
  `/cskill:review` (thin `context: fork` entry points to each agent).
- `cs-planner` agent (opus) that enforces complete, unambiguous plans.
- Security bug class added to `cs-reviewer` focus.
- First seeded skill from a `/skill-save` verification run.

### Changed
- `cs-reviewer` now runs cheap checks (smoke import, single test) instead of
  reading only; routed to haiku.

## [0.1.0]

### Added
- Initial release: mini, token-frugal orchestration plugin — lean agents,
  cheap-model routing, `/cskill:auto` autopilot, and `/cskill:skill-save`.
