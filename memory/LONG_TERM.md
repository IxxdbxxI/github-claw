# Long-Term Memory

> Persistent facts that survive across all sessions.
> Edit to update; almost never delete.
> Last updated: 2026-04-29

---

## Owner

- GitHub handle: IxxdbxxI
- Preferred language for docs/chat: Chinese and English (bilingual OK)
- Repository: `IxxdbxxI/github-claw`

## Workspace Purpose

This repository is a personal AI workspace where Claw (the resident assistant) maintains
continuity across GitHub Copilot sessions through files.

## Preferences

- Keep documentation concise; avoid over-engineering.
- Commit small, focused changes.
- Use this repo as a persistent memory store — anything important goes in a file.

## Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-04-29 | Initialized workspace with `AGENTS.md` + `memory/` | First-time setup per issue request |
| 2026-04-29 | Added `.agents/skills/` skill system | Stable skill discovery, installation, and usage mechanism for Claw |
| 2026-04-29 | Added Issue automation workflow with `COPILOT_ASSIGNEE` variable | Auto-acknowledge Issues and route bugs to Copilot coding agent |

## Known Context

- No existing code or tooling in the repo (only `README.md` at init time).
- No CI, linters, or tests configured yet — add structure only when needed.
- Issue automation workflow comments on new Issues and assigns Copilot for bugs (via `COPILOT_ASSIGNEE`).

## Skill System

- Skills live in `.agents/skills/<skill-name>/`, each with `skill.yml` + `README.md`.
- `_template/` is the canonical template for new skills.
- Claw must discover skills at session start by reading `.agents/skills/` directory.
- Installing a skill = creating its directory + committing to the repo.
