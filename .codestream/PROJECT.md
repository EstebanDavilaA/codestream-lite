# PROJECT

Project specifics live here, in one place, so `RULES.md` can stay generic.

## What this is

<One paragraph: what the app is, who uses it, what it's for.>

## Stack

<Language, runtime, framework, database, package manager.>

## Where things live

<The handful of directories that matter and what each holds.>

## The checks (rule 4)

Every one of these runs before a build is reported as passing, and every exit
code is reported.

| Check | Command |
|---|---|
| tests | `<command>` |
| typecheck | `<command>` |
| build | `<command>` — or `N/A` and why |
| lint | `<command>` |

## Known constraints

<Anything a session must not do. Migrations that must be used. Files that are
protected. Environment quirks — e.g. "run Python as `uv run python`, never bare
`python3`".

## Known open defects

<A pointer to `.codestream/BUGS.md`. Keep the list there, not here.>
