# <Milestone> / Wave <name>

**Date:** YYYY-MM-DD · **Status:** PLANNING | AWAITING SPEC_APPROVED | BUILDING stage <n> | AWAITING /steer | CHECKPOINT
**Branch:** `wave/<milestone>-<name>` (created at approval)

> Coordination only. What each phase delivers is in its spec; nothing here restates it.

## Lanes

| Stage | Phase | Spec | Approval | Status |
|---|---|---|---|---|
| 1 | P<n> | `.codestream/active/<milestone>-P<n>-<slug>.md` | pending / approved | drafted / blocked on P<n> / building / built / merged / reviewed |

## Ownership

Each lane edits only the files it owns. A file no lane owns is out of bounds for every lane.

| Phase | Owns (rewrites) | May only add to (shared) |
|---|---|---|
| P<n> | paths or globs | e.g. a guardrail's coverage list, a package's exports |

## Why this staging

One line per stage boundary: which phase needs whose output, or which file two lanes would both rewrite.

## Approval

Record the user's approval by phase. Only approved, dependency-ready phases may run; unapproved phases stay pending, and approved phases with unmet prerequisites stay blocked. The wave remains open until every listed phase is merged or explicitly removed by the user.

## Runner's log

Dated one-liners: merges, the check exit codes after each, conflicts and how they were settled.
