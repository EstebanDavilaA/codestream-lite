# <Milestone> / Phase <N> — <name>

**Date:** YYYY-MM-DD · **Status:** DRAFT

> One page. If it doesn't fit, the phase is doing too much — split it.

## What you can do after this phase

- Three to six plain sentences. Observable outcomes only: what the user can do,
  see, or stops having to do. No types, no file paths, no measurements.

## What we are not building

- One line each. Anything not listed above and not listed here is out of scope
  by default. Naming the exclusions is what stops scope creep at review time.
- If something is deliberately deferred, say where it goes instead.

## Ambiguous — needs a decision

Only include questions where the answer changes what gets built. Delete the
section if there are none.

### Q1 — <the decision, one sentence>

**Context:** what's happening, in plain words, with the numbers that matter.

**Why it matters:** what changes depending on the answer.

**Options:** A) … B) … — recommended: A, because …

## Rules and patterns that apply

Named references only. Never restated here.

- e.g. `state machine` — `DESIGN_PATTERNS#3`
- e.g. no database migration this phase
- e.g. the MCP provider's read path stays untouched

## How we will know it works

Five to fifteen checks, each an observable outcome a person or a test can
perform. These are what the reviewer walks through item by item.

- [ ] Pressing Start shows a running state naming the endpoint URL
- [ ] Stopping releases the port
- [ ] Closing the app leaves no server listening
- [ ] …

---

## Notes for whoever writes this spec

- Describe what the user can do. The code is the source of truth for the code.
- Never put a hash, byte count, schema version, file count, line number or
  measured duration in here. Those describe a moment, and the moment passes.
- If a check needs a measurement, take it at run time and compare it to another
  measurement taken at run time.
- Name the rules and patterns that apply. Don't explain them.
