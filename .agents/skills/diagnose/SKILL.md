---
name: diagnose
description: Find the cause of a failure before anything is patched — wrong code, wrong spec, or wrong idea. Use whenever a build fails, a check goes red, or a bug is reported.
---

# Diagnose

Don't let anyone — including yourself — jump to a patch. There are three causes,
they need three different fixes, and patching at the wrong layer reproduces the
same bug a milestone later.

## The three causes

| Cause | Looks like | Fix at |
|---|---|---|
| Wrong code | the spec is right; the code doesn't do it | the code |
| Wrong spec | the code does what the spec said, and the spec was wrong | the spec: correct it, re-approve, rebuild |
| Wrong idea | the spec matches what was asked; what was asked was wrong | the goal |

## Process

1. **Read the failing artifact from disk, in full.** The code, the test, the data.
   Not a summary, not your memory of it.

2. **Ask whether the code does what the spec said.** If it doesn't — wrong code.

3. **If it does, ask whether the spec was right.** If it wasn't — wrong spec.
   Correct it, get it re-approved, then rebuild. Don't patch the code against a
   spec that's still wrong; you'll just move the gap.

4. **If the spec was faithful to what was asked and the result is still wrong** —
   wrong idea. Go back to `.codestream/DISCOVERY.md` and fix it there.

5. **Say it before touching anything:**

   ```
   CAUSE:    wrong code | wrong spec | wrong idea
   WHY:      one or two sentences
   GOES TO:  where the fix belongs
   ```

6. **Route it there.** Don't fix one layer down because it's quicker.

## Things worth recognising

- **A requirement describing the machine rather than the software** — a hash, a
  byte count, a schema version, a file count. These break when the user uses the
  product. The fix is to delete the requirement, not to freeze the machine.
- **A test asserting something the user can legitimately change.** Same defect,
  same fix.
- **A clause that contradicts another clause in the same document.** Nothing in
  the process checks pairs, so read the spec as a whole before blaming the code.
- **A "measured" claim in a spec that the measurement contradicts.** Somebody
  recorded what they saw once and wrote it down as a requirement.
