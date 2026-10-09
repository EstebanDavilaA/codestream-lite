---
name: plan
description: Draft the one-page spec for the next slice, using .codestream/templates/spec.md, then halt for SPEC_APPROVED. No code is written until the user says the literal word.
---

# Plan

Write one page. Get it approved. Nothing gets built before the word.

## Process

1. **Read only the relevant context**: `RULES.md` rule 3, the spec template,
   the applicable discovery and roadmap entries, and relevant parts of
   `PROJECT.md`. Read code only where it affects the proposed outcome.

2. **Understand the request.** Summarize the problem and a proposed approach in
   plain language, using only context the user needs to make the decision. Don't
   restate internal documents or make the user chase references.

3. **Resolve material decisions interactively.** Ask through the interactive
   question UI when an unanswered choice would change user-visible behavior or
   scope. Explain the problem, why it matters, concise options, and a
   recommendation. Ask only what cannot be answered from the conversation or
   project; never treat the recommendation as the user's decision. Record each
   answer in the resulting outcomes or exclusions, not as a permanent open
   question section.

4. **Place the phase in its milestone.** Find the milestone's required phases in
   `ROADMAP.md`. Say at the top of the spec which phase this is, and which phases
   remain after it (or that it is the last). Then check the list against the
   milestone's scope and verification threshold:
   - if this phase is too big, split it and add the new phases to the roadmap;
   - if the spec reveals work the list doesn't cover, add the phase to the roadmap;
   - if the milestone needs no phase beyond this one, say so.

   Correct the roadmap's list in the same session, dated, and tell the user in the
   spec what you changed.

5. **Draft from the template.** If it doesn't fit on a page, the phase is doing
   too much. Split it; don't shrink the font.

6. **Check it against rule 3.** No hash, no byte count, no schema version, no file
   count, no line number, no measured duration. Name the rules and patterns that
   apply; never restate them. Cover the primary user journey and only the
   edge-case behavior that materially changes what the user can do, see, or risk.
   Keep outcomes and checks concise and non-duplicative. If available, run
   `bin/codestream lint spec <spec-path>` (or MCP `codestream_lint_spec`) to statically
   verify required sections and rule 3 anti-patterns before presenting.

7. **Present and stop.** Give the user a short summary of the problem, approach,
   recommendation, delivered outcomes, and exclusions. If a material decision
   remains, ask it interactively and update the spec before presenting the final
   approval request. Wait for `SPEC_APPROVED`; do not build.

## If the spec turns out to be wrong later

Correct it at the top of the same file with a dated note: what was wrong, what it
says now, and what forced the change. Don't rewrite the original text — the record
of what was approved is the point of keeping it. Then get it re-approved before
anyone builds against the correction.

## Do not

- No code. Not a line, not a stub, not "just the types".
- No acceptance-criteria ids, no coverage table, no clause labels. The spec's
  *How we will know it works* list is the entire matrix.
- Don't ask decisions the user has already answered or the project can resolve.
- Don't start `/execute` after presenting. Present, then stop.
- Don't turn speculative edge cases into requirements or duplicate context to
  make the spec look comprehensive.

## When asked to plan or implement a wave

A request to plan or implement multiple phases together belongs in `/wave`, not
in a single-phase `/plan`. The wave runner plans every selected phase and stops
for approval before any build begins. When the request doesn't identify one
milestone and its desired phases clearly, ask which milestone and phases to
include or exclude before creating the manifest or spawning planners. Use the
roadmap to resolve scope only when it leaves one clear interpretation; don't
guess between milestones or treat unrelated phases as one wave.

## As a lane in a wave

When `/wave` runs you, you're one of several planners working at once. The process
above still applies, with these differences:

- Write **only** your own spec file. Don't edit `ROADMAP.md`, `STATE.json` or the
  manifest; the runner does that once for every lane.
- Read the manifest and the other lanes' phases. Where your slice meets theirs
  (a shared component, a coverage list, a token), say in the spec which side owns
  the element. Never assume the other lane does it.
- Don't halt for approval yourself. Return to the runner:
  1. the spec's path, its concise problem/approach/outcomes/exclusions summary,
     and any material decisions still requiring the runner to ask the user;
     don't write an unresolved decision into the final spec as if its
     recommendation were approved;
  2. the files you expect to **rewrite** and the shared files you expect only to
     **add to**, measured by reading the code, not guessed;
  3. anything you need from another lane's output (that's a stage boundary);
  4. any roadmap correction you would have made, worded as you'd write it.
