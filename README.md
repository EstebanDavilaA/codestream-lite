# CODESTREAM-lite

A spec-gated, vertical-slice framework for AI coding assistants, reduced to the
seven rules that earn their keep.

It's a fork of CODESTREAM, rewritten after measuring where the original spent its
effort. "Why this exists" below is a set of numbers, not a preference.

---

## The seven rules

They live in [`RULES.md`](RULES.md) — the only normative file here. Short version:

1. **One slice at a time.** Every phase ships something you can open the app and use.
2. **A phase starts only after a one-page spec is approved.**
3. **The spec describes outcomes, never code** — and never a measurement of the machine.
4. **Build it, then run the project's checks.** All of them, with exit codes.
5. **Whoever checks it must not be whoever built it.**
6. **When something fails, find the cause before patching.**
7. **Stop at the checkpoint.**

## The lifecycle

```
/onboard → /prototype → (user validates) → /roadmap ─┐
                                                      │
/onboard → /discover → /roadmap ──────────────────────┼─→ /plan →
                                                              [SPEC_APPROVED] →
                                          /execute (checks, halts) → /steer ────┐
                                          (review passes) → checkpoint          │
                                          (fails) → /diagnose → back to /execute, /plan, or /discover
```

| Command | What it does |
|---|---|
| `/prototype` | One question, then a minimal working slice. |
| `/discover` | Intent questions → `DISCOVERY.md`. No code. |
| `/roadmap` | What exists → `ROADMAP.md`, as vertical slices. |
| `/plan` | The one-page spec. Halts for `SPEC_APPROVED`. |
| `/execute` | Builds the slice, runs the checks, halts. |
| `/steer` | Independent review, then the checkpoint. |
| `/diagnose` | Cause before patch. |
| `/log` | Bugs and ideas, with enough context to act on. |
| `/research` | Read-only answers. |

---

## Why this exists

Measured against the original framework after 11 phases, 2026-09-10 → 2026-09-23:

| Symptom | Number |
|---|---|
| Rules text — the same ~28 rules, written four times | 142 KB |
| Skill files, 14 of them duplicated across two directories | 42 |
| Framework docs, excluding archives | 441 KB |
| Binding clauses in one phase's spec, for a phase that built 3 files | 126 |
| Clauses in that spec that were unsatisfiable | ~6% — six, four of them contradicting other clauses in the same document |
| Critic verdicts: FAIL | 9 of 17 |
| `/diagnose` verdicts classified "spec error" vs "implementation bug" | 6 vs 2 |
| Bugs logged | 13 — of which 8 were defects in the framework's own artifacts |
| Bugs found by using the app | **0** |

The number that matters most is the last one. A framework whose bug log is fed
entirely by agents reading documents is a framework that verifies paperwork. The
one severe product bug it did catch — a transfer that silently destroyed the
amount it moved — it found *by accident*, because an unrelated clause happened to
claim both balances moved.

The conclusion those numbers point at: the cost was dominated by the artifact the
framework forced you to produce, not by the gates it ran. Specs grew to 126
clauses because each rule pushed precision into more assertions — a rule demanding
a row per sub-clause mechanically multiplied them, and nothing checked whether any
two of them could both be true.

So this version keeps the parts that demonstrably worked — vertical slices,
independent review, cause-before-patch, the checkpoint — and deletes the rest.
`RULES.md` ends with the list of what was removed and why, so it doesn't creep
back in a future session.

---

## What's here

```
RULES.md                           the whole framework — read this first
CLAUDE.md                          directives for Claude Code
.agents/AGENTS.md                  directives for everything else
.github/copilot-instructions.md    directives for GitHub Copilot

.agents/skills/<verb>/SKILL.md     ten skills, one per verb

.codestream/
  PROJECT.md                       project specifics: what it is, the check commands
  STATE.json                       milestone, phase, short session log
  ROADMAP.md, DISCOVERY.md         intent, and the order it gets built in
  BUGS.md, FEATURES.md             what's broken, what's wanted
  templates/spec.md                the one-page spec
  templates/DESIGN_PATTERNS.md     reference — named by specs, never restated in them
  templates/UX_HEURISTICS.md       reference — same
  archive/                         superseded material, kept, never rewritten

.codestream-template               marks this directory as the framework's source
```

## Adopting it

1. Copy `RULES.md`, `CLAUDE.md`, `.agents/`, `.github/` and `.codestream/` into the
   project root.
2. **Delete `.codestream-template`.** That marker makes `/onboard` refuse to run,
   by design — it stops the framework running its own lifecycle inside its own
   source directory.
3. Fill in `.codestream/PROJECT.md`: the four check commands, and anything a
   session must not do.
4. Set your agent id in whichever directive file your tool reads.
5. Run `/onboard`.

Keep the framework in its own commit, separate from app code. Framework churn
should never look like a change to the product — and once your code is in git,
`git diff` does the job the old file manifests were invented to do.
