---
name: sdd
description: Defines complete workflow from specification through testing to implementation.
---

The workflow is defined as code in [workflow.py](workflow.py).

## Questions

Ask every `ask_user` in `workflow.py` before the first `run_skill`, on every path.

1. In one prompt with the AskUserQuestion tool, ask the development-or-skill, prototype-or-full, engineering-or-data, and change type questions. Offer `feat`, `fix`, `perf`, and `refactor` as the change type options. The user types `test`, `docs`, `style`, `chore`, `ci`, or `build` through Other.
2. Then ask "What do you want to build? Type done when finished." as a plain chat message. Do not use the AskUserQuestion tool. Wait for the reply. Repeat until the user answers `done`.

- Ask the engineering-or-data and change type questions every time, even for a prototype.
- No `run_skill` runs until both steps are done.

## Yolo mode

The user starts yolo mode by running the skill with `yolo` and a goal, like `yolo add a --json flag`. In yolo mode, `yolo` is true and `goal` is the goal.

- Never ask the user, and never use the AskUserQuestion tool. Answer every `ask_user` from the goal.
- When no requirements are left, answer `done` to the requirement question.
- Keep going until the goal is complete. Decide every choice inside a skill yourself.
- Do not bypass hooks or protected files. If a change is blocked, skip it and report it at the end.
