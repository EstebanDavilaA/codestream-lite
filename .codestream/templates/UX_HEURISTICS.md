# UX Heuristic Reference

Reference material for `/plan`, `/execute` and the reviewer in `/steer`, whenever a
slice touches user-facing UI.

A UX claim is worth writing down only if someone can tell whether it holds:

1. **The spec names the two or three heuristics actually load-bearing** for what's
   being built — not all ten, every time — in *Rules and patterns that apply*,
   with the concrete behaviour and the anti-pattern it forbids.
2. **At least one item in *How we will know it works* can fail** for each one. A
   code-level check (a disabled-state guard, an ARIA attribute, a non-empty
   tooltip) counts. "It feels clear" doesn't.
3. **The build honours it**, with no shortcuts: no silent failure standing in for
   a visible error, no blocking action with no signal that something is
   happening.
4. **The reviewer exercises the actual behaviour** (rule 5) rather than reading
   the code and inferring compliance, then classifies findings using the shared
   severity and checkpoint policy in `RULES.md`.

---

## Severity Scale

Use these levels for UX and other review findings. Severity describes impact;
verification status separately describes whether an outcome was verified,
failed, or remains unverified. The same level determines whether a finding blocks
the checkpoint, under `RULES.md`:

- **Critical** — a core user journey cannot be completed, or there is a severe security, safety, accessibility, or data-integrity risk.
- **Major** — an important outcome fails, a significant regression occurs, or substantial friction prevents reliable task completion.
- **Minor** — an inconvenience with a reasonable workaround; the agreed outcome remains achievable.
- **Advisory** — an optional improvement that does not materially affect task completion.

Critical and Major findings block and route through `/diagnose` (rule 6).
Minor and Advisory findings do not block; report them and log worthwhile
follow-up as a `FEATURE`. An unverified result is not automatically a failure:
it blocks only when missing evidence leaves a material outcome or risk
unresolved.

---

## Quick-Reference: Nielsen's 10 Heuristics + Accessibility Floor

| # | Heuristic | Anti-Pattern to Catch | Useful review evidence |
|:--|:---|:---|:---|
| 1 | Visibility of System Status | Async action with no loading/progress indicator; state change with no visible confirmation | `Verification` |
| 2 | Match Between System and the Real World | Jargon, error codes, or internal terminology surfaced directly to the user | `Verification` |
| 3 | User Control and Freedom | No cancel/undo/escape from a multi-step or destructive flow | `Verification` |
| 4 | Consistency and Standards | The same action (e.g. "delete") behaves or is labeled differently across screens | `Structure` |
| 5 | Error Prevention | A destructive action has no confirmation step; a form allows an invalid submission the backend will reject anyway | `Verification` |
| 6 | Recognition Rather Than Recall | User must remember a value shown on a prior screen instead of it staying visible/selectable | `Verification` |
| 7 | Flexibility and Efficiency of Use | No keyboard path or shortcut for a frequent action a mouse-only flow forces | `Verification` |
| 8 | Aesthetic and Minimalist Design | Irrelevant or redundant information competing with the task at hand | `Verification` |
| 9 | Help Users Recognize, Diagnose, and Recover from Errors | Generic error message ("Something went wrong") with no specific cause or next step | `Structure` |
| 10 | Help and Documentation | A non-obvious feature has no in-context help where one is needed to complete the task | `Verification` |
| A11y | Accessibility Floor | Missing ARIA label on an interactive element; focus state not visible; color contrast below WCAG AA; keyboard trap | `Structure` / `Lint` |

---

## Worked Examples

### 1. Visibility of System Status

- **Target Smell:** A button triggers a network request with no visual change until the response resolves; the user clicks again, assuming nothing happened.
- **Spec Norm Declaration Example:**
  > `Norm: All async mutations show a loading state within 100ms of trigger and a success/error confirmation on completion. The trigger control is disabled for the duration of the request. Precedent: .codestream/templates/UX_HEURISTICS.md#1-visibility-of-system-status`
- **Review evidence:** Trigger the action (or inspect a recorded interaction); confirm a visible state transition occurs before resolution, not just after.

### 2. Help Users Recognize, Diagnose, and Recover from Errors

- **Target Smell:** A failed request surfaces "An error occurred" with no indication of what failed or what the user should do.
- **Spec Norm Declaration Example:**
  > `Norm: Every user-triggered error state names the specific cause and offers a concrete next action (retry, edit the invalid field, contact support), never a bare generic message. Precedent: .codestream/templates/UX_HEURISTICS.md#9-help-users-recognize-diagnose-and-recover-from-errors`
- **Review evidence:** Trigger representative failure modes; confirm the rendered message explains the problem and a useful next step.

### 3. Consistency and Standards

- **Target Smell:** Three screens implement "delete" as three different confirmation flows (one inline, one modal, one instant with no confirmation).
- **Spec Norm Declaration Example:**
  > `Norm: Destructive actions across this phase's screens use the shared confirmation-modal component; no screen implements its own inline or instant-delete variant. Precedent: .codestream/templates/UX_HEURISTICS.md#4-consistency-and-standards`
- **Review evidence:** Exercise destructive actions across the touched screens; confirm behavior is consistent and gives the user an appropriate chance to cancel.

---

## The YAGNI Guardrail

> [!WARNING]
> **Do not gate on UX polish that has no bearing on task completion.**
> This file exists to catch friction that blocks or confuses users, not to enforce aesthetic taste.
> - A slice with no user-facing UI (a CLI tool, a backend script, a data migration) cites nothing here — there is no interaction to audit.
> - A `Minor` or `Advisory` concern (spacing, tooltip wording, non-blocking tab-order improvement) belongs in `/log` as a `FEATURE` entry, not as a blocker — don't force a halt over cosmetic polish.
> - A genuinely small change (rule 2's exception) skips heuristic extraction entirely. Make the change and say what you did.
