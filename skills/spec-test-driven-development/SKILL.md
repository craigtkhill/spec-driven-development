---
name: spec-test-driven-development
description: Defines complete workflow from specification through testing to implementation.
---

The workflow is defined as code in [workflow.py](workflow.py).

## Questions

Ask every `ask_user` in `workflow.py` before the first `run_skill`, on every path.

1. In one prompt with the AskUserQuestion tool, ask the development-or-skill, prototype-or-full, and engineering-or-data questions.
2. Then ask "What do you want to build? Start with feat, fix, test, docs, refactor, style, chore, perf, ci, or build." as a plain chat message. Do not use the AskUserQuestion tool. The reply is a commit type and a description, like `perf make parsing faster`. The type is the commit type for that requirement. Wait for the reply. Repeat until the user gives a blank answer.

- Ask the engineering-or-data question every time, even for a prototype.
- No `run_skill` runs until both steps are done.
