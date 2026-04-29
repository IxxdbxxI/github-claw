# github-claw

Personal AI workspace powered by GitHub Copilot.

**Claw** is the resident AI assistant living in this repository.
It maintains identity, memory, and working context across sessions through versioned files.

## Quick Start

- [`AGENTS.md`](./AGENTS.md) — read this first: role definition, workflow, memory rules
- [`memory/LONG_TERM.md`](./memory/LONG_TERM.md) — persistent context
- [`memory/LOG.md`](./memory/LOG.md) — session activity log

## How It Works

Every Copilot session begins by reading `AGENTS.md`.
Completed work is logged in `memory/LOG.md` and committed back to the repo,
so context accumulates rather than disappearing after each conversation.