---
name: onboard
description: Entry point for a session. Reads the project state, routes to the right command, and stops. Use at the start of work in a project using this framework, or when the user asks where to start or what's next.
---

# Onboard

Read the state, pick the track, hand off. Build nothing here.

## Process

1. **Check framework health and route.** If available, run `bin/codestream status --json`
   (or MCP `codestream_status`). It deterministically verifies framework integrity,
   guards against running in `.codestream-template`, validates `STATE.json`, checks
   active artifact constraints, and returns the recommended route in a single compact call.
   If running without the CLI:
   - Check this isn't the framework's own source (`.codestream-template`).
   - Confirm `RULES.md` is present.
   - Read `.codestream/STATE.json`. If it doesn't parse as JSON, stop — that's
     corruption, not something to work around. If the newest `state_history` entry
     belongs to a *different* agent and its step isn't finished, stop and say so
     rather than guessing whether that session is done.

2. **Work out where the project is:**

   | State | Route to |
   |---|---|
   | No state file, or an empty history | Ask what we're building → `/prototype` or `/discover` |
   | A raw idea, nothing validated | `/prototype` |
   | A clear idea, no roadmap | `/discover`, then `/roadmap` |
   | A roadmap, no active spec | `/plan` for the next slice |
   | An approved spec, nothing built | `/execute` |
   | A build finished, awaiting review | `/steer` |
   | A spec or roadmap waiting on the user | Present it, say what you're waiting for, stop |
   | `artifacts.active_wave` is set | `/wave`, at the stage its manifest's status names |

   For an active wave, corroborate `building` labels with available lane
   completion reports and Git ancestry before declaring execution unfinished.
   Completed but unmerged lanes route to `/wave`'s interrupted-handoff recovery;
   merged lanes with failed or missing checks route to integration/diagnosis,
   not review. Report the evidence and route only; do not merge during onboard.

4. **Say the state in one short paragraph** — milestone, phase, what's next — then
   stop. If the next step needs the user's word, ask for it.

## Do not

- Don't start building. Not one line.
- Don't "tidy up" state that looks stale. Say what you see and ask.
- Don't read the whole archive. `STATE.json` and the current spec are enough.
