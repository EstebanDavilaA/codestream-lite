---
name: prototype
description: Build a minimal working slice from a raw, unvalidated idea, fast, to find out whether the idea is worth building properly. Use when the user describes something new without asking for a formal spec.
---

# Prototype

The point is to find out cheaply whether the idea is worth building. Optimise for
speed and for something runnable. Not code quality, not completeness, not tests.

## Process

1. **Ask one question** — the one whose answer most changes what you'd build. Use
   the question format in `RULES.md`: question, context, why it matters, options
   with a recommendation.

2. **Build the smallest thing that proves the idea.** One screen, one flow, one
   end-to-end path. Fake whatever is expensive, and say what you faked.

3. **Make it run.** Give the user the exact command to start it.

4. **Say plainly what's real and what isn't.** "The ledger part works against a
   real database; the categories are hardcoded" is the kind of sentence that makes
   a prototype useful.

5. **Stop and ask whether it's worth building properly.** If yes, `/roadmap` turns
   it into real slices.

## Rules

- No spec, no roadmap, no tests, no state file ceremony. That's the point.
- Don't gold-plate. A prototype that took a week has failed.
- Delete-worthy code is fine. Say that it is.
- If the prototype shows the idea is wrong, that's a success — say so clearly
  rather than rescuing it.
