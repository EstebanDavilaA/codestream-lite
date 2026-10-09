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
- assess whether the agreed user outcome is met, not whether implementation
  wording literally mirrors the spec
- report each outcome as **verified**, **failed**, or **unverified**, with concise
  evidence; an unverified outcome is never marked passed
- report unrequested behavior and missing artifacts, explaining their user impact
  rather than treating every deviation as an automatic failure
- classify findings using the shared severity policy in `RULES.md`; distinguish
  blockers from non-blocking polish and harmless deviations

### 2. Run scoped checks

Run targeted checks for the changed behavior and focused integration checks
against the current application state. Select broader regression checks when the
change crosses components, changes shared behavior, has significant regression
risk, or reaches a milestone boundary. Do not rerun every earlier milestone's
suite by default at each phase. Report commands run with actual exit codes,
checks deferred with reasons, and any remaining risk. A deferred check is not a
pass.

### 3. Decide whether the review blocks

Critical or major failures block the checkpoint: for example, an approved
material outcome fails, the core journey is broken, a significant regression is
present, or a security, safety, accessibility, or data-integrity risk remains.
An unverified material outcome blocks only when the missing evidence leaves its
success or an important risk unresolved. Route blockers through `/diagnose`;
don't patch during `/steer`.

Minor or advisory findings, wording differences that preserve the agreed
outcome, and harmless isolated deviations do not block. Report them and log
useful follow-up as appropriate. An unrequested change blocks only if it is
harmful, risky, or materially changes agreed scope.

If any blocker remains, report the evidence, route it through `/diagnose`, and
stop without presenting a checkpoint. When no blockers remain, present a
checkpoint even if it includes non-blocking findings or clearly stated
verification limitations.

### 4. If no blockers remain

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
Outcome evidence: <verified / failed / unverified summary>
Checks: <commands and exit codes; deferred checks with reasons>
Non-blocking findings and remaining limitations: <items, or "none">

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

**Readiness preflight comes before reviewers.** Check the manifest, available
lane completion reports, and Git ancestry on the wave branch. A stale `building`
label does not prove a lane is unfinished; an idle execution session does not
prove completion either. If reported lane commits are unmerged, explain that
execution finished but runner integration remains, and route to `/wave`'s
interrupted-handoff recovery under the existing approval. Do not review an
isolated lane as the combined wave. If every lane is already merged, reconcile
stale labels from the evidence and verify the required merged checks. Missing
reports, unfinished lanes, unresolved conflicts, or failed merged checks must
be resolved through `/wave` or `/diagnose` before calling the wave ready.

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
3. **Run targeted and integration checks** against the merged wave branch:
   cover each lane's changed behavior and interactions across lanes. Select
   broader regression checks when the combined change crosses components or has
   significant risk; run the full historical suite at the milestone boundary.
   Report actual exit codes and deferred checks with reasons. Do not rerun all
   earlier milestone suites by default.
4. **Every finding is recorded.** Defects outside any spec's scope go through
   `/log`. Failures go to `/diagnose` (see `/wave` step 4).
5. **One checkpoint**, with a line per phase and outcome verification status,
   blockers separated from non-blocking findings, check results and limitations,
   and the milestone count as in step 4. No phase with a blocking failure is
   presented as done; if some passed and some failed, say so, and offer to
   re-review only the fixed ones.

## Do not

- Never advance past the checkpoint on your own, however obvious the next step
  looks.
- Don't present a checkpoint while material blockers remain. Report
  non-blocking findings and verification limits transparently.
- Don't review it yourself and call the result independent.
