---
name: log
description: Record a bug in .codestream/BUGS.md or a feature idea in .codestream/FEATURES.md, with enough context that the next reader re-derives nothing.
---

# Log

Write it down now, so nobody has to choose between scope creep and forgetting.

## Process

1. **Bug or feature?** Broken behaviour → `BUGS.md`. A capability that doesn't
   exist yet → `FEATURES.md`.

2. **Read the file, then append.** Never rewrite an existing entry. Next id:
   `BUG-0nn` or `FEAT-0nn`.

3. **Fill the template properly.** "It doesn't work" isn't an entry. What you did,
   what happened, what you expected — with the real numbers. A future session
   should be able to act on this without asking you anything.

4. **Say how you found it.** "Using the app" is the most valuable answer there is.
   If the log is only ever fed by document-reading, that's worth saying out loud —
   a bug log about paperwork isn't a bug log about the product.

5. **Say where the fix belongs** if you know — the code, a spec correction, or the
   goal (rule 6).

## When it doesn't deserve an entry

A typo, a stale comment, a one-word fix: just fix it and say what you did (rule
2's exception). The log is for things a future session needs to know about, not
for everything you touched.
