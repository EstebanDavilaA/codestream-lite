---
name: roadmap
description: Cut the work into vertical-slice milestones in .codestream/ROADMAP.md. Use after /discover, or to audit an existing codebase and plan forward from what's actually there.
---

# Roadmap

Produce `.codestream/ROADMAP.md`: ordered milestones, each one something a user
can run. This is also the path for an existing codebase — understand what's there,
then plan forward from it.

## Process

If there is code already:

1. **Read what exists, and use the app if you can.** Note what works and what
   doesn't. Running it will tell you more than reading it.
2. **Read `.codestream/BUGS.md`.** Open defects outrank new capability. If the
   user has been using the app and has a list of what's broken, that list is the
   most valuable input you have — put a milestone in front of new features.

Then:

3. **List the outcomes the product needs**, in the order they unlock each other.
   A milestone that can't unlock the next one is probably in the wrong place.
4. **Resolve material decisions with the user interactively** before committing
   to a roadmap direction. Explain the problem, why it matters, options, and a
   recommendation in plain language; do not require the user to inspect internal
   documents. Don't ask what the conversation or code already answers.
5. **Check each one is a vertical slice** (the test below). Split or drop the ones
   that aren't.
6. **Name the exclusions** for each milestone — the tempting adjacent things that
   are deliberately not in it. Naming them here is what stops them appearing
   mid-build.
7. **Include the important user scenarios.** State the main journey and only
   those failure or edge cases that materially change user-visible behavior,
   safety, or data. Assign each in-scope outcome to a phase or explicitly exclude
   it; don't enumerate hypothetical cases or duplicate phase specs.
8. **List the required phases for each milestone.** A milestone is done when its
   phases are done, so say which phases those are: a numbered list, one line each,
   naming what that phase delivers and the milestone's verification threshold item
   it satisfies. Every part of the milestone's scope and threshold must land in
   some phase; a part with no phase is a gap, so add the phase or cut the part.
   One phase is a legitimate answer; say so rather than padding.
9. **Present and stop.** Summarize the problem, proposed roadmap approach,
   recommendation, milestone outcomes, key scenarios, and exclusions. Ask any
   remaining material decision through the interactive question UI, update the
   roadmap with the answer, then wait for roadmap approval. Don't start planning
   a phase.

## Keeping the phase list true

The list is a working commitment, not a forecast. `/plan` and `/steer` re-read it,
and either may find it wrong. When they do, the roadmap is corrected in the same
session, with a dated note saying what changed and why, and the user is told at
the next gate. A milestone's phase list that nobody updated is how a milestone gets
closed with work missing, or kept open with none left.

## The test for a slice

Ask: *when this is done, what can I open the app and do?*

If the answer is "nothing yet, but the types are in place", it isn't a slice.
Horizontal layering — all the models, then all the services, then all the UI — is
the most common way a plausible-looking roadmap produces nothing demonstrable for
weeks.

## Also

- Name the phases, and keep the count honest, or say it is unknown. A stale number
  is worse than no number.
- Don't promise a phase count you can't justify. "Estimate, not a promise" is a
  perfectly good thing to write, as long as the phases you can already name are
  listed.
- Read only the project context needed to ground the roadmap. Avoid copying
  discovery or code details into it when a concise user outcome is enough.
