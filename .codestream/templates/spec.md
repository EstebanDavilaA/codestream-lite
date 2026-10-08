# <Milestone> / Phase <N> — <name>

**Date:** YYYY-MM-DD · **Status:** DRAFT

> One page. If it doesn't fit, the phase is doing too much — split it.

## Problem

One or two plain-language sentences on what is missing or painful and for whom.

## Proposed approach

One or two sentences on the intended user-facing direction and recommendation.
Keep implementation design in the code unless the user has approved a constraint.

## What you can do after this phase

- Three to six plain sentences. Observable outcomes only: what the user can do,
  see, or stops having to do. No types, no file paths, no measurements.
- Include the primary use case and only material edge cases that change the
  user's experience, safety, or data. Fold the behavior into these outcomes.

## What we are not building

- One line each. Anything not listed above and not listed here is out of scope
  by default. Naming the exclusions is what stops scope creep at review time.
- If something is deliberately deferred, say where it goes instead.

## Rules and patterns that apply

Named references only. Never restated here.

- e.g. `state machine` — `DESIGN_PATTERNS#3`
- e.g. no database migration this phase
- e.g. the MCP provider's read path stays untouched

## How we will know it works

Checks a person or test can perform for the primary journey and material
edge-case behavior. These are what the reviewer walks through item by item.
Keep them distinct, observable, and limited to what matters; don't duplicate
the outcomes as a second exhaustive requirements list.

- [ ] Pressing Start shows a running state naming the endpoint URL
- [ ] Stopping releases the port
- [ ] Closing the app leaves no server listening
- [ ] …

---

## Notes for whoever writes this spec

- Describe what the user can do. The code is the source of truth for the code.
- Resolve material decisions with the user before asking for approval, then
  record the decision as settled scope in the outcomes or exclusions.
- Read only the project context needed to understand the slice. Don't copy
  background detail into the spec or repeat the same behavior in multiple
  sections.
- Never put a hash, byte count, schema version, file count, line number or
  measured duration in here. Those describe a moment, and the moment passes.
- If a check needs a measurement, take it at run time and compare it to another
  measurement taken at run time.
- Name the rules and patterns that apply. Don't explain them.
