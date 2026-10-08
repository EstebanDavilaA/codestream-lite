---
name: wave
description: Run several phases of one milestone in parallel — plan them all, get one approval, build each in its own worktree, merge, then review them all in one /steer. Use when the user asks to parallelise phases, or STATE.json names an active wave.
---

# Wave

The runner of a wave coordinates it and builds nothing. It fans out `/plan`, then
`/execute`, then `/steer` to lanes, integrates what they return, and owns the
framework's shared files. `RULES.md` *Running phases in parallel* is the
contract; this is the procedure.

A **lane** is one phase run by a subagent or a separate session. A **stage** is the
set of lanes that run at once. Later stages start only after the earlier ones are
merged.

## 0. Cut the wave

1. Run the *Starting a session* guards. If `active/` holds a spec, it either joins
   the wave (say why), or the wave waits for it.
2. Inspect `git status` before creating wave artifacts. If there are uncommitted
   or untracked changes, stop and ask the user to commit or otherwise resolve
   them first. Never silently include, omit, commit, stash, or discard them. At
   execution time, verify that no unexpected changes have appeared; only the
   wave's approved specs, manifest, state update, and planning roadmap
   corrections may be committed on the wave base.
3. Identify the target milestone and phases from the request and `ROADMAP.md`.
   If either is ambiguous, ask which milestone and phases to include or exclude
   before proceeding. For each selected phase pair, ask: would they rewrite the
   same file? Does one need the other's output? Either answer puts them in
   different stages.
4. Write the manifest from `.codestream/templates/wave.md` to
   `.codestream/active/<milestone>-WAVE-<name>.md`. Ownership is a first guess at
   this point; the planners correct it.
5. Point `artifacts.active_wave` at it and append a `STATE.json` entry.

## Before anything runs in parallel

- **Every checkout runs the same dependency versions.** A worktree resolves its own
  environment; if the lockfile isn't committed it resolves *different* versions, and
  every render and test in it describes a program the user doesn't run. Commit the
  lockfile first, or stop and ask.
- **Every agent gets its own scratch subfolder**, named for its lane or review.
  Agents share the scratch root, and one agent's cleanup must never reach another's.
- **Usage limits stop whole stages at once.** If the tool has one, start fewer agents
  at a time rather than resuming many.

## 1. Plan — every lane at once

Spawn one planner per phase, all in parallel, with no worktree: each writes
only its own spec file. Give each one:

- its phase, its spec path, the manifest path, and the other lanes' phases;
- the instruction to follow `/plan` *as a lane* (the section at the end of that
  skill).

When they've all returned, the runner:

- reads every spec from disk, and checks it against rule 3 and against the others
  (two specs claiming one element, or each assuming the other does it, is a
  finding);
- fixes the manifest's ownership from what the planners actually found in the code,
  and re-stages any pair that now overlaps;
- applies the roadmap corrections the planners proposed — once, dated;
- consolidates material unresolved decisions across lanes and asks the user
  interactively, in plain language, before final approval. Explain the problem,
  why the choice matters, concise options, and a recommendation; don't ask the
  user to interpret a manifest or internal references. Record answers as settled
  outcomes or exclusions in the affected specs;
- presents the wave with a concise problem/approach summary, per-lane outcomes
  and exclusions, key user scenarios, stage order, and approval status. Don't
  duplicate the full specs in the summary. State that implementation starts only
  after approval. Then **stop**.

Only after material decisions are resolved and written into the specs, wait for
`SPEC_APPROVED` or `WAVE_APPROVED` (rule 2's wave form).

## 2. Execute — one worktree per lane

`SPEC_APPROVED` for a wave authorises exactly these git steps and no others:

1. Commit the approved specs, manifest, wave's `STATE.json` update, and any
   roadmap corrections produced during planning on a new branch
   `wave/<milestone>-<name>` off the current branch — the **wave base**. The
   dirty-tree preflight must have passed; do not commit other working-tree
   changes as part of this step. Lanes branch from the wave base, so they read
   the approved specs and current framework state from their own checkout.
2. For each lane in the current stage, spawn an executor in its own worktree on
   `wave/<milestone>-<name>-<phase>` — a sibling, not a child: git can't hold both `wave/M12-B` and `wave/M12-B/P3` (Claude Code: the agent tool's `worktree`
   isolation; elsewhere: `git worktree add`). Tell it to follow `/execute` *as a
   lane*, and to commit its work on its own branch.
3. As each lane returns: read its report, check its diff stays inside the files the
   manifest gives it, and merge it into the wave branch. Additive conflicts in shared
   files (both sides add a list entry, an import, an export) are resolved by keeping
   both sides. Any other conflict: stop — the cut was wrong (see `RULES.md`).
4. After every merge, run all of `PROJECT.md`'s checks on the wave branch and record
   the exit codes. A lane that was green alone and is red merged hasn't passed.
   Worktrees separate files, not the machine: tests that scan processes or bind
   fixed ports collide when two checkouts run them at once. A red result while any
   lane is running checks isn't evidence either way; run the checks again when no
   lane is running them, and only that run counts.
5. When a stage is merged and green, start the next stage from the wave branch.
   A lane that stops without a report (a crash, a usage limit, a closed session)
   hasn't finished: look at its worktree, then resume it with its context if the
   tool allows, or start a fresh lane in the same worktree that reads the diff
   first. Never merge a lane that hasn't reported.
6. Write what the lanes reported: one `STATE.json` entry per lane, their `/log`
   items to `BUGS.md` / `FEATURES.md`.

For partial approval, record approval per phase in the manifest. Run only
explicitly approved phases whose prerequisites are approved and complete.
Unapproved phases remain pending; approved phases with an unmet prerequisite
remain blocked, not implicitly approved. After each approved stage is green,
stop and ask for approval of any still-unapproved phases. Previously approved
blocked phases may run once their prerequisites are approved and complete. Do
not start `/steer` or call the wave built while any listed phase remains pending
or blocked. If the human wants to exclude such a phase, update the manifest to
remove it before closing the wave.

Once every listed phase is merged and green, stop and say the wave is built and
waiting for `/steer`. Don't review it.

## 3. Steer — once, for the whole wave

Run `/steer` with the manifest. It walks the wave form of that skill: one fresh
reviewer per spec in parallel, one integration reviewer, one regression run, and a
single checkpoint listing every phase.

## 4. When the review finds something

`/diagnose` each failure and route it:

- **wrong code** → a fix lane: the same phase, re-entered in a new worktree off the
  wave branch, scoped to the findings. No re-approval needed.
- **wrong spec** → correct the spec (dated), and get `SPEC_APPROVED <phase>` before
  its fix lane runs.
- **wrong idea** → take it to the human. It may take the phase out of the wave.

Fix lanes can run in parallel under the same ownership rules. Afterwards, `/steer`
again for only the phases that changed, plus the integration reviewer.

## 5. Close

At the checkpoint, the human merges the wave branch into the main branch, or asks
you to. Then the specs move to `.codestream/archive/specs/`, the manifest with them,
`artifacts.active_wave` is cleared, and the worktrees and lane branches are removed.

## Do not

- Don't let a lane write `STATE.json`, `ROADMAP.md`, `BUGS.md` or `FEATURES.md`.
- Don't merge into the main branch. Don't push.
- Don't start a later stage on an unmerged or red wave branch.
- Don't have the runner build, or review, any lane.
- Don't resolve a non-additive conflict by picking a side.
