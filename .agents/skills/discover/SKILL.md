---
name: discover
description: Ask what we're building, for whom, and why, and write the answers to .codestream/DISCOVERY.md. No code, no architecture, no stack proposals, no file trees.
---

# Discover

Turn an idea into a written statement of intent. You write exactly one file:
`.codestream/DISCOVERY.md`.

## Process

1. **Read the DISCOVERY.md template.** It is your question list.

2. **Ask the questions that matter, a few at a time.** Each one carries its own
   context, in the format from `RULES.md`:

   ```
   QUESTION:        the decision, one sentence
   CONTEXT:         what's happening, in plain words, with the numbers that matter
   WHY IT MATTERS:  what changes depending on the answer
   OPTIONS:         A) …  B) …  — recommended: A, because …
   ```

3. **Answer what you can yourself** by reading the codebase. Only ask the user
   what only the user knows. Asking someone something you could have looked up
   wastes the one resource you can't get more of.

4. **Write DISCOVERY.md.** Short enough that somebody will actually read it.

5. **Stop.** Turning intent into milestones is `/roadmap`, a separate step.

## Do not

- No code. No stack proposals. No file trees. No architecture.
- Don't ask ten questions when three will do.
- Don't ask a question whose answer is already in the conversation — write down
  what was said and confirm it.
