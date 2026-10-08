---
name: research
description: Answer a question — feasibility, trade-offs, what the codebase actually does, or whether a document or another repo is worth adopting — without changing code or writing specs.
---

# Research

Read-only. The output is an answer, not an artifact.

## Process

1. **Work out what the question actually is.** "Can we do X" and "should we do X"
   need different answers, and the user may not have separated them. Say which one
   you're answering.

2. **Gather evidence, not opinions.** Read the code, run the thing, measure it.
   Say which parts are measured and which are judgement.

3. **Answer plainly:** what's true, what's uncertain, and what you'd need to find
   out to be sure.

4. **If the question is "should we", say what it costs** — roughly how many
   slices, what it would break, and what it displaces. A feature that costs three
   phases and breaks nothing is a different proposal from one that costs three and
   rewrites the ledger.

## Evaluating something from outside

If the user hands you a document or another repo to compare against this project:

- Say what it **actually does** — not what it claims, and not what its README
  says it will do one day.
- Say what's worth taking, and as what: a rule, a skill, a template, a test, a
  pattern.
- Say what this project **already does**, so you don't propose it twice.
- Say what to avoid, and why.

Then stop. Deciding to adopt something is the user's call, and it's a different
conversation from evaluating it.

## Do not

- Don't write code, specs, or state. If the answer implies a change, say what and
  hand off to `/plan` or `/log`.
- Don't pad the answer. A short correct answer beats a thorough vague one, and
  it's the difference between a research note someone reads and one they don't.
