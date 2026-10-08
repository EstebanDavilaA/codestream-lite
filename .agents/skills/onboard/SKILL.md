---
name: onboard
description: Entry point for a session. Reads the project state, routes to the right command, and stops. Use at the start of work in a project using this framework, or when the user asks where to start or what's next.
---

# Onboard

Read the state, pick the track, hand off. Build nothing here.

## Process

1. **Check this isn't the framework's own source.** If `.codestream-template`
   exists at the repo root, stop and say so — this directory is the framework,
   not a project built with it, and running a feature through it would bake
   project content into every future project that copies it. If `RULES.md` itself
   is missing, stop and say that too.

2. **Read `.codestream/STATE.json`.** If it doesn't parse as JSON, stop — that's
   corruption, not something to work around. If the newest `state_history` entry
   belongs to a *different* agent and its step isn't finished, stop and say so
   rather than guessing whether that session is done.

3. **Work out where the project is:**

   | State | Route to |
   |---|---|
   | No state file, or an empty history | Ask what we're building → `/prototype` or `/discover` |
   | A raw idea, nothing validated | `/prototype` |
   | A clear idea, no roadmap | `/discover`, then `/roadmap` |
   | A roadmap, no active spec | `/plan` for the next slice |
   | An approved spec, nothing built | `/execute` |
   | A build finished, awaiting review | `/steer` |
   | A spec or roadmap waiting on the user | Present it, say what you're waiting for, stop |

4. **Say the state in one short paragraph** — milestone, phase, what's next — then
   stop. If the next step needs the user's word, ask for it.

## Do not

- Don't start building. Not one line.
- Don't "tidy up" state that looks stale. Say what you see and ask.
- Don't read the whole archive. `STATE.json` and the current spec are enough.
