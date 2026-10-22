---
name: prototyping
description: Use before writing code for a prototype. Defines the short path: the repo's existing language (Python, or TypeScript for frontend, when the repo shows no clear pattern), then the write-code skill, skipping specs, tests, and the rest of the workflow.
---

# Prototyping

A prototype is quick code to try an idea. Use the short path.

## Language

Stay in the language the repo already uses. Match its existing code, tooling, and conventions.

Only when the repo shows no clear language pattern, use this as a starting suggestion:
- Frontend code: TypeScript
- Anything else: Python

## Rules

- The `write-code` skill runs next. This skill runs before it.

## Skip

Do not run any other skill from the workflow:
- Specifying requirements
- Writing tests
- Error handling
- Refactoring
- Pre-commit hooks
- Commit messages
