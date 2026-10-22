---
name: spec-test-driven-development
description: Defines complete workflow from specification through testing to implementation.
---

The workflow is defined as code in [workflow.py](workflow.py).

## Questions

Ask every `ask_user` in `workflow.py` before the first `run_skill`.

1. In one prompt, ask the development-or-skill, prototype-or-full, and engineering-or-data questions.
2. For full, then ask each requirement, one per prompt, until the user gives a blank answer.

- Do not stop after step one. Run step two when the user picks full.
- Ask the engineering-or-data question every time, even for a prototype.
- No `run_skill` runs until both steps are done.
