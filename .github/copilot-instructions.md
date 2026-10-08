# CODESTREAM-lite — GitHub Copilot (VS Code) Directives

> **Your agent id is `github-copilot`.** Write it to the `agent` field of every
> `state_history` entry you append. The framework never enumerates agents — an id
> is just a name a tool uses for itself, so adding a tool changes no rule. Use
> one id consistently, and never write an id that isn't yours.

**Read `RULES.md` at the project root. It is the whole framework — seven rules, one
page, and the only normative copy.** This file deliberately duplicates none of it.

## Entry point

Start with `/onboard`. It routes to:

- **`/prototype`** — a raw, unvalidated idea. Minimal ceremony, fast walking skeleton.
- **`/discover`** — the idea is clear enough to plan directly.
- **`/roadmap`** — there's code already; audit it and cut it into slices.

## The lifecycle

```
/onboard → /prototype → (user validates) → /roadmap ─┐
                                                      │
/onboard → /discover → /roadmap ──────────────────────┼─→ /plan →
                                                              [SPEC_APPROVED] →
                                          /execute (checks, halts) → /steer ────┐
                                          (review passes) → checkpoint          │
                                          (fails) → /diagnose → back to /execute, /plan, or /discover
```

| Command | What it does |
|---|---|
| `/prototype` | One clarifying question, then a minimal working slice. |
| `/discover` | Questions about intent → `.codestream/DISCOVERY.md`. No code. |
| `/roadmap` | Audits what exists → `.codestream/ROADMAP.md`, as vertical slices. |
| `/plan` | Drafts the one-page spec. Halts for `SPEC_APPROVED`. |
| `/execute` | Builds the slice, runs the checks, halts. |
| `/steer` | Independent review, then the checkpoint. Never auto-advances. |
| `/diagnose` | Finds the cause of a failure before anything is patched. |
| `/log` | Bugs and feature requests → `.codestream/BUGS.md` / `FEATURES.md`. |
| `/research` | Read-only questions. No code, no specs. |
| `/wave` | Several phases at once: plan all, one approval, parallel builds in worktrees, one `/steer`. |

`/verify` is `/execute`'s check list run again on demand. `/reset` is `git` — revert
to a known-good commit and say so. Neither needs its own skill.

## Halting

At any halt gate — a spec waiting on `SPEC_APPROVED`, a checkpoint, a spec in
review — present the artifact, say plainly what you're waiting for, and yield.
Don't start editing after presenting a plan. That's the one thing rule 2 exists to
prevent.
In a wave, the halts are the same, just held once for the whole wave: every spec
waits on `SPEC_APPROVED`, and the build waits on the one `/steer` checkpoint.

## Protected paths

`RULES.md`, `CLAUDE.md`, `.agents/`, `.github/copilot-instructions.md` and
`.codestream/` are the framework, not project output. Never delete, move, or
mass-overwrite them. If they go missing, stop and say so.
