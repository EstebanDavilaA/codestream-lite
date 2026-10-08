---
name: execute
description: Build the approved spec's slice, run the project's checks, report every exit code, and halt for the user to run /steer. It does not review its own work.
---

# Execute

Build what the spec says. Nothing else.

## Process

1. **Read the spec from disk, in full, at the moment you start.** Not from
   context — a file that was right when written can be wrong when read.

2. **Build the slice.** Follow the patterns the spec names.

3. **Run every check in `.codestream/PROJECT.md`** — tests, typecheck, build,
   lint. Report each one's real exit code. Where a check doesn't apply, write
   "N/A — no build step in this project". Silence isn't the same as not
   applicable.

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
