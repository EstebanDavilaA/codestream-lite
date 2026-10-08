---
name: plan
description: Draft the one-page spec for the next slice, using .codestream/templates/spec.md, then halt for SPEC_APPROVED. No code is written until the user says the literal word.
---

# Plan

Write one page. Get it approved. Nothing gets built before the word.

## Process

1. **Read** `RULES.md` rule 3, `.codestream/templates/spec.md`,
   `.codestream/DISCOVERY.md`, `.codestream/ROADMAP.md` and
   `.codestream/PROJECT.md`.

2. **Read the code the slice touches.** A spec written without reading the code
   produces clauses that can't be satisfied — this is the single most common
   source of wasted build cycles.

3. **Place the phase in its milestone.** Find the milestone's required phases in
   `ROADMAP.md`. Say at the top of the spec which phase this is, and which phases
   remain after it (or that it is the last). Then check the list against the
   milestone's scope and verification threshold:
   - if this phase is too big, split it and add the new phases to the roadmap;
   - if the spec reveals work the list doesn't cover, add the phase to the roadmap;
   - if the milestone needs no phase beyond this one, say so.

   Correct the roadmap's list in the same session, dated, and tell the user in the
   spec what you changed.

4. **Draft from the template.** If it doesn't fit on a page, the phase is doing
   too much. Split it; don't shrink the font.

5. **Check it against rule 3.** No hash, no byte count, no schema version, no file
   count, no line number, no measured duration. Name the rules and patterns that
   apply; never restate them.

6. **Ask the open questions in the spec itself** — question, context, why it
   matters, options, recommendation. A decision left implicit becomes a build
   cycle lost.

7. **Stop.** Present the spec and wait. If any question is still unanswered,
   the spec is not ready for `SPEC_APPROVED`: list each open question, wait for
   the human's answers, and write them into the spec. Only once none is open,
   wait for the literal `SPEC_APPROVED`.

## If the spec turns out to be wrong later

Correct it at the top of the same file with a dated note: what was wrong, what it
says now, and what forced the change. Don't rewrite the original text — the record
of what was approved is the point of keeping it. Then get it re-approved before
anyone builds against the correction.

## Do not

- No code. Not a line, not a stub, not "just the types".
- No acceptance-criteria ids, no coverage table, no clause labels. The spec's
  *How we will know it works* list is the entire matrix.
- Don't ask a question without context (see the question format in `RULES.md`).
- Don't start `/execute` after presenting. Present, then stop.

## As a lane in a wave

When `/wave` runs you, you're one of several planners working at once. The process
above still applies, with these differences:

- Write **only** your own spec file. Don't edit `ROADMAP.md`, `STATE.json` or the
  manifest; the runner does that once for every lane.
- Read the manifest and the other lanes' phases. Where your slice meets theirs
  (a shared component, a coverage list, a token), say in the spec which side owns
  the element. Never assume the other lane does it.
- Don't halt for approval yourself. Return to the runner:
  1. the spec's path, and its open questions by title;
  2. the files you expect to **rewrite** and the shared files you expect only to
     **add to**, measured by reading the code, not guessed;
  3. anything you need from another lane's output (that's a stage boundary);
  4. any roadmap correction you would have made, worded as you'd write it.
