---
name: discover
description: Ask what we're building, for whom, and why, and write the answers to .codestream/DISCOVERY.md. No code, no architecture, no stack proposals, no file trees.
---

# Discover

Turn an idea into a written statement of intent. You write exactly one file:
`.codestream/DISCOVERY.md`.

## Process

1. **Read the DISCOVERY.md template** and relevant project context.

2. **Ask only what the user must decide.** Use the interactive question UI when
   available. Explain the problem and why the decision matters in plain language,
   give concise options and a recommendation, and ask one decision at a time.
   Don't require the user to inspect internal docs or answer questions that can
   be resolved from the conversation or project.

3. **Answer what you can yourself** by reading the codebase. Only ask the user
   what only the user knows. Asking someone something you could have looked up
   wastes the one resource you can't get more of.

4. **Write DISCOVERY.md** with settled intent: the problem, audience, observable
   success, and exclusions. Do not preserve answered questions as an open Q&A
   section. Keep it short enough that somebody will actually read it.

5. **Present and stop.** Summarize the problem, proposed direction, and
   recommendation plainly, then wait. Turning intent into milestones is
   `/roadmap`, a separate step.

## Do not

- No code. No stack proposals. No file trees. No architecture.
- Don't ask ten questions when three will do.
- Don't ask a question whose answer is already in the conversation — write down
  what was said and confirm it.
