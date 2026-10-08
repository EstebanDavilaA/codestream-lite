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

1. **Read the relevant artifacts from disk.** Read the approved outcome, the
   affected code, and the concrete review or test evidence. Expand to related
   code only as needed to understand the behavior; don't re-audit unrelated
   history.

2. **Reproduce or validate the material finding.** Establish what the user
   actually experiences and what the evidence can and cannot prove. A wording
   difference is not a failure when the agreed user outcome is met.

3. **Ask whether the implementation meets the agreed outcome.** If not, and the
   outcome is sound, diagnose wrong code.

4. **If the implementation matches the spec but the spec is wrong, incomplete,
   or self-contradictory** — diagnose wrong spec. Correct it, get it re-approved,
   then rebuild. Don't patch code against a spec that's still wrong.

5. **If the spec faithfully represents what was asked but the result is still
   wrong** — diagnose wrong idea. Go back to `.codestream/DISCOVERY.md` and fix
   the goal.

6. **Say it before touching anything:**

   ```
   CAUSE:    wrong code | wrong spec | wrong idea
   WHY:      one or two sentences
   GOES TO:  where the fix belongs
   ```

7. **Route material blockers to the right layer.** Don't patch a non-blocking
   Minor or Advisory finding as if it were a failure; report or log it instead.
   Don't fix one layer down because it's quicker.

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
