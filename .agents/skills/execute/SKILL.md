---
name: execute
description: Build the approved spec's slice, run the project's checks, report every exit code, and halt for the user to run /steer. It does not review its own work.
---

# Execute

Build what the spec says. Nothing else.

## Process

1. **Read the spec from disk, in full, at the moment you start.** Not from
   context — a file that was right when written can be wrong when read.
   Build only from its settled outcomes and exclusions. If implementation reveals
   a material unanswered decision or conflict with the user's intent, stop and
   return to `/plan` to resolve it interactively and update the spec; do not
   assume the recommended approach answers for the user.

2. **Build the slice.** Follow the patterns the spec names.

3. **Run the relevant checks in `.codestream/PROJECT.md`** for the changed
   behavior and its current integration surface. Report each command and its
   actual exit code; say why a project check is not applicable. Do not claim
   skipped checks passed. Run the full historical suite at a milestone boundary
   or when the breadth or risk of the change warrants it, as rule 4 describes.

4. **Confirm what changed** with `git diff --stat`. Anything outside the spec:
   say so. Don't quietly leave it in and don't quietly take it out if the spec
   wanted it.

5. **Log the step** to `.codestream/STATE.json` — read the file, parse it, append,
   write, re-parse to confirm. Say what you built, the check results, and that
   you're waiting on `/steer`.

6. **Stop.** Say the build is done and you're waiting for the review.

## Do not

- Don't review your own work, or run the reviewer yourself. Rule 5 exists because
  the author's tests encode the author's misunderstandings.
- Don't fix what you notice along the way unless the spec says to. Log it with
  `/log` — that's what it's for, and it saves you choosing between scope creep and
  forgetting.
- Don't touch anything the spec puts out of bounds.
- Don't report a check as passing without its exit code.

## As a lane in a wave

When `/wave` runs you, you're in your own git worktree, on your own branch. The
process above still applies, with these differences:

- Read your spec **and** the manifest from your checkout. Edit only the files the
  manifest gives your phase. A shared file you may only add to: add, never rewrite
  or reorder. If the slice needs a file outside your ownership, stop and report it;
  don't edit it.
- Don't write `STATE.json`, `ROADMAP.md`, `BUGS.md` or `FEATURES.md`. Put what you
  would have logged in your report instead, worded so the runner can paste it.
- Run targeted checks in your worktree for your changed behavior and its
  integration surface, and commit your work on your branch with the phase in the
  message. Report broader checks you did not run; never imply they passed.
- Return to the runner, instead of halting: what you built, every check's exit
  code, `git diff --stat` against the wave base, anything outside the spec, and the
  `/log` items.
