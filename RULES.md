# RULES

Seven rules. They are the framework. Everything else here is a process for
applying them.

Read this once. A session shouldn't need to read it twice.

---

## 1. One slice at a time

Every phase ships something you can open the app and use. Not types, not an API,
not a UI shell — something usable end to end.

If a phase can't be described as "after this, you can do X", it isn't a phase.
Split it.

## 2. A phase starts only after a one-page spec is approved

The spec uses `.codestream/templates/spec.md`. It fits on a page. If it doesn't,
the phase is doing too much.

The literal word `SPEC_APPROVED` from the human starts the build. Nothing else
does.

**Open questions block approval.** A spec with an unanswered question in its
*Ambiguous — needs a decision* section is not ready. Present it as waiting on
those answers, name each open question, and do not accept or act on
`SPEC_APPROVED` until the human has answered every one and the answers are
written into the spec. Never assume a recommended option.

**A genuinely small change skips all of this.** One file, no new capability, no
new behaviour — just do it and say what you did. Don't perform ceremony on a
one-line fix. If it turns out to be bigger than that, stop and route it back
through this rule.

## 3. The spec describes outcomes, never code

A clause says what the user can do or see. It never:

- restates a rule or a design pattern — it names it (`state machine`,
  `DESIGN_PATTERNS#3`) and moves on
- restates a type, signature, constant list, or file tree — the code is the
  source of truth for the code
- records a measurement of the machine: a hash, a byte count, a schema version,
  a file count, a line number, a duration. Those describe a moment, and the
  moment passes. If a check needs a measurement, it takes the measurement at run
  time and compares it to another measurement taken at run time.

**This is the rule that matters most.** The previous version of this framework
lacked it, and specs grew to 126 clauses for a phase that built three files.
About 6% of those clauses were unsatisfiable, four of them because they
contradicted *other clauses in the same document*, and every one cost a build
cycle. None described anything a user could see. Fold a number into a clause and
you've created a requirement that the user breaks simply by using the product.

## 4. Build it, then run the project's checks

`.codestream/PROJECT.md` lists the commands. All of them run, and every exit code
is reported. A green test suite with a broken build is not a pass.

If a check doesn't apply — no build step, no typechecker — say so in those words.
Silence isn't the same as "not applicable".

## 5. Whoever checks it must not be whoever built it

The builder's tests are evidence, not proof. A test written by the same agent that
wrote the code encodes the same misunderstandings.

So a fresh context reads the spec, reads the code, runs the real thing, and walks
the spec's own **How we will know it works** list item by item. It reports which
items it couldn't verify and why, and anything built that the spec didn't ask for.

This is the highest-value step here. It has caught a bug that silently destroyed
money on every transfer, a user-visible string describing the opposite of what
the program did, and a server process still listening after its owner was gone.
Don't skip it, and don't run it in the context that just finished building.

## 6. When something fails, find the cause before patching

Three causes, three different fixes:

| Cause | What it looks like | Fix at |
|---|---|---|
| Wrong code | the spec is right; the code doesn't do it | the code |
| Wrong spec | the code does what the spec said; the spec was wrong | the spec: correct it, re-approve, rebuild |
| Wrong idea | the spec matches what was asked; what was asked was wrong | the goal |

Patching at the wrong layer reproduces the same bug a milestone later. State the
cause before touching anything:

```
CAUSE:    wrong code | wrong spec | wrong idea
WHY:      one or two sentences
GOES TO:  where the fix belongs
```

## 7. Stop at the checkpoint

After the checks pass and the independent review is done, present the result and
stop. Never advance on your own, however obvious the next step looks.

---

## Starting a session

1. If `.codestream-template` exists at the repo root, stop — that's the
   framework's own source, not a project.
2. Read `.codestream/STATE.json`. If the newest entry belongs to a *different*
   agent and its step is unfinished, stop and say so rather than guessing whether
   that session is done.
3. If `STATE.json` doesn't parse as JSON, or the active spec isn't valid UTF-8,
   stop. That's cross-tool corruption; don't work around it.

## Asking a question

Every question carries its own context. A question that names an id and nothing
else isn't a question, it's a test.

```
QUESTION:        the decision, one sentence
CONTEXT:         what's happening, in plain words, with the numbers that matter
WHY IT MATTERS:  what changes depending on the answer
OPTIONS:         A) …
                 B) …
RECOMMENDED:     A, because …
```

Ask when the answer changes what gets built. Don't ask to confirm what the spec
already says, and don't ask something you could answer by reading the code.

## Protected paths

`.codestream/`, `.agents/`, `.github/copilot-instructions.md`, `CLAUDE.md` and
this file are the framework, not project output. No skill, subagent or scaffolding
step may delete, move, or mass-overwrite them — including "clean slate"
scaffolding (`npm create`, `django-admin startproject` and friends). If a tool
would wipe the target directory, run it in a temp directory and copy only the app
files in. If these paths go missing, stop and say so.

## State

`.codestream/STATE.json` holds the current milestone, phase, and a short log of
what each session did. Keep it small — the last handful of entries, not the
project's whole history. Older entries are worth keeping; move them to
`.codestream/archive/STATE_HISTORY.md` rather than leaving them inline.

The active spec lives in `.codestream/active/` as `<milestone>-<phase>-<slug>.md`,
and `STATE.json`'s `artifacts.active_spec` points at it. There is at most one file
in `active/` — if there are two, stop and say so rather than guessing which one is
current. **The one exception is a wave** (below): then `active/` holds the wave's
manifest and exactly the specs it lists, and `artifacts.active_wave` points at the
manifest. A spec in `active/` that the manifest doesn't list is the same stop.

## Running phases in parallel (a wave)

A wave is several phases of one milestone planned together, built in parallel, and
reviewed once. It applies the seven rules; it suspends none of them. `/wave` runs it.

- **Rule 1 holds per phase.** Each phase in a wave is still its own slice with its
  own spec.
- **Rule 2 holds per wave.** Every spec is drafted, its questions answered, and
  then the human approves the wave with `SPEC_APPROVED` (or its alias
  `WAVE_APPROVED`) — which, said to a wave, approves every spec its manifest lists,
  or only the phases named after it (`SPEC_APPROVED P3 P4`). A spec with an open
  question can't be approved by either form. Answers given in the same message as
  the word are written into the specs first; then the word acts.
- **The manifest decides what may run at once.** It lists each phase's lane, the
  code it owns, and the shared files it may only add to. Two lanes that would
  rewrite the same file don't share a stage. A phase that needs another's output
  goes in a later stage of the same wave.
- **Lanes don't write the framework's shared files.** `STATE.json`, `ROADMAP.md`,
  `BUGS.md` and `FEATURES.md` belong to whoever runs the wave. A lane reports what
  it would have written there, and the runner writes it once.
- **Each lane builds in its own git worktree,** on a branch off the wave's branch.
  The runner merges finished lanes into the wave's branch, re-runs every check
  after each merge (rule 4), and never merges into the main branch — that's the
  human's step, at the checkpoint.
- **Rule 5 holds per phase.** One `/steer` reviews the whole wave, with one fresh
  reviewer per spec and one more for what only shows up once the lanes are
  together. The checkpoint (rule 7) comes once, for the wave.
- **A merge conflict that isn't purely additive means the wave was cut wrong.**
  Stop, and treat it as rule 6's wrong spec. Don't settle it by choosing a side.

---

## What this framework deliberately doesn't have

Each of these existed in the previous version and was removed. They're listed so
nobody re-adds them by accident:

- **An acceptance-criteria matrix with ids.** Replaced by the spec's own *How we
  will know it works* checklist — same coverage, no id bookkeeping, no `Verifies`
  columns, no `Mapped to AC-…` prose.
- **A rule against "derived literals" plus a checker scanning for them.** Rule 3
  covers the real problem in one sentence, and covers the case that rule missed.
- **A mechanical coverage gate** (`check-spec-coverage.py`). It inflated clause
  counts by demanding a row per sub-clause, and couldn't see the parts of the spec
  where the defects actually lived.
- **File manifests** — hashes of every file before and after a phase, to prove
  which files changed. `git diff` does this. Commit your work.
- **A spec-reconciliation table** labelling every clause. The reviewer reports
  clauses with no artifact as findings instead.
- **An amendment log** with numbered entries and quoted old/new text. A short
  dated correction at the top of the same file is enough.
- **A persona layer** — a second skill per verb (`plan_spec`, `execute_feature`,
  `audit_critic`, …) restating its parent. One skill per verb.
- **Four copies of these rules.** This file is the only normative copy. The three
  directive files each hold an agent id, the protected paths, and a pointer here.
