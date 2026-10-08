---
name: steer
description: Independently review a finished build against the spec, then present the checkpoint and stop. The review runs in a fresh context, never in the one that built the code.
---

# Steer

Two jobs: get the build independently checked, then hand the decision to the human.

## Process

### 1. Review, in a fresh context

A subagent, or a new session. Never the context that just finished building
(rule 5). Give the reviewer the spec path and tell it to walk *How we will know it
works* item by item.

The reviewer should:

- read the spec and the code from disk, in full
- run the real thing where it can, rather than reading the tests and inferring
- try to break the assumptions the builder made silently
- report anything built that the spec didn't ask for
- report anything the spec asked for that has no artifact
- say which items it could **not** verify, and why — not mark them passed

### 2. Check for regressions

Run the checks from `.codestream/PROJECT.md` again, plus whatever the earlier
milestones' suites cover. Report real exit codes.

### 3. If the review fails

Don't patch, and don't present a checkpoint. Run `/diagnose` and hand it the
findings. A failed review is information about the spec as much as the code —
that's what rule 6 is for.

### 4. If it passes

Present the checkpoint and stop:

```
[CHECKPOINT]

Done and checked: <one or two sentences>

Waiting on you:
- A) Refine — tell me what to adjust in this phase.
- B) Next phase — move on to the next slice.
- C) Adjust the roadmap — change what's coming, based on what we learned.
- D) Milestone done — close it out and start the next one.
```

## Do not

- Never advance past the checkpoint on your own, however obvious the next step
  looks.
- Don't present a checkpoint for work that failed review. Say it failed and why.
- Don't review it yourself and call the result independent.
