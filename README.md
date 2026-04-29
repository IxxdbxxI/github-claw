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

## Issue Automation

This repo includes an Issue workflow that:

- Replies to every newly opened Issue with a short confirmation and info request.
- Assigns bug Issues to the GitHub Copilot coding agent so it can open a fix PR.

**Configuration (required):**

- Set a repository variable `COPILOT_ASSIGNEE` to the Copilot coding agent login
  (e.g. `github-copilot[bot]` or your org’s Copilot agent account).

**Bug detection rules (auto-assign):**

- Issue has a `bug`-type label, **or**
- Issue body includes clear bug template sections: steps to reproduce + expected + actual behavior
  (supports English/Chinese keywords).
