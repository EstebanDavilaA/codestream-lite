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

3. **Draft from the template.** If it doesn't fit on a page, the phase is doing
   too much. Split it; don't shrink the font.

4. **Check it against rule 3.** No hash, no byte count, no schema version, no file
   count, no line number, no measured duration. Name the rules and patterns that
   apply; never restate them.

5. **Ask the open questions in the spec itself** — question, context, why it
   matters, options, recommendation. A decision left implicit becomes a build
   cycle lost.

6. **Stop.** Present the spec and wait for the literal `SPEC_APPROVED`.

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
