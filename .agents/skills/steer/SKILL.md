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

First, work out where the milestone stands. Read the milestone's entry in
`ROADMAP.md` — its required phases, scope and verification threshold — and check
each against what is now built and verified:

- which required phases are done, and which remain;
- whether every part of the milestone's scope and threshold is met by finished
  phases, or still open;
- whether this phase showed that the list is wrong (a missing phase, a phase that
  is no longer needed). If so, correct the roadmap now, dated, and say so.

Then present the checkpoint and stop:

```
[CHECKPOINT]

Done and checked: <one or two sentences>

Milestone <n>: <phases done> of <phases required> done.
Remaining: <each remaining phase, one line> — or "none: the scope and threshold
are met".
<Any roadmap correction made, or "roadmap unchanged".>

Waiting on you:
- A) Refine — tell me what to adjust in this phase.
- B) Next phase — move on to the next slice. (Only if a phase remains in this
  milestone.)
- C) Adjust the roadmap — change what's coming, based on what we learned.
- D) Milestone done — close it out and start the next one. (Only if no phase
  remains; otherwise say which are left.)
```

Say which of B or D the evidence points to. If the user picks B when no phase
remains, or D while one does, say so and ask before going on: B would cross a
milestone boundary without closing it, and D would close a milestone with work
missing.

### 5. At milestone done (option D)

Before closing the milestone, check that its work is committed: `git status` shows
no uncommitted changes to the milestone's files. If any remain, halt and say so;
ask the user to commit or to say to go on without. Never commit on your own.

## For a wave

When the manifest in `artifacts.active_wave` names the build, one `/steer` reviews
every phase in it, on the wave branch:

1. **One fresh reviewer per spec, in parallel.** Each gets its spec path and the
   instructions in step 1 above, and walks only its own *How we will know it works*.
   Each reviews an export of the wave branch (`git archive <commit>` into its own
   scratch subfolder), not a worktree: a worktree with no changes can be removed when
   its agent stops, and an export carries no live data. A reviewer never relaunches
   the app from the main checkout.
2. **One integration reviewer**, also fresh. It looks for what no single spec can
   see: two lanes styling one element differently, a shared file a merge left
   inconsistent, an element each spec assumed the other built, and the milestone's
   verification threshold across every screen the wave touched.
3. **One regression run** of every `PROJECT.md` check on the wave branch, with
   exit codes.
4. **Every finding is recorded.** Defects outside any spec's scope go through
   `/log`. Failures go to `/diagnose` (see `/wave` step 4).
5. **One checkpoint**, with a line per phase (passed, or failed and why) and the
   milestone count as in step 4. No phase is presented as done while it failed
   review; if some passed and some failed, say so, and offer to re-review only the
   fixed ones.

## Do not

- Never advance past the checkpoint on your own, however obvious the next step
  looks.
- Don't present a checkpoint for work that failed review. Say it failed and why.
- Don't review it yourself and call the result independent.
