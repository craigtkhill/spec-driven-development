---
name: spec-test-driven-development
description: Defines complete workflow from specification through testing to implementation.
---

The workflow is defined as code in [workflow.py](workflow.py).

## Questions

Ask every `ask_user` in `workflow.py` before the first `run_skill`. No `run_skill` runs until all questions are answered.

- A question inside an `if` is asked right after the answer it depends on, as a follow-up prompt. For example, ask engineering or data after the user picks full.
- Do not stop after the first batch of questions. Check the code for questions that still apply.
- Keep asking a `while ask_user` question until the user gives a blank answer.
