[Skills Index]|roots: .claude/skills,.codex/skills,.opencode/skills,.pi/skills
|IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning for any skill tasks.
|spec-test-driven-development:{SKILL.md}
|specifying-requirements:{SKILL.md}
|acceptance-test:{SKILL.md}
|test-driven-development:{SKILL.md,PYTHON.md,RUST.md}
|write-code:{SKILL.md}
|prototyping:{SKILL.md}
|refactoring-code:{SKILL.md,FILE-ORGANIZATION.md,RUST.md}
|write-commit-message:{SKILL.md}
|install-dependencies:{SKILL.md,PYTHON.md,RUST.md,TYPESCRIPT.md}
|update-dependencies:{SKILL.md,PYTHON.md}
|evaluation:{SKILL.md}
|create-skill:{SKILL.md}
|pre-commit-hooks:{SKILL.md,RUST.md}
|error-handling:{SKILL.md}

## 🚨 CRITICAL PRE-FLIGHT CHECK 🚨

**BEFORE writing ANY code, making ANY edits, or implementing ANYTHING:**

1. **STOP** - Do not proceed directly to implementation
2. **CHECK** - Review the Skills Index above
3. **MATCH** - Identify if ANY skill applies to the user's request
4. **INVOKE** - Use the Skill tool FIRST (this is MANDATORY, not optional)

**NO EXCEPTIONS**: Even with detailed plans, even with clear instructions, ALWAYS check and use skills first.

## Overview

This repository contains reusable skills for software development workflows using specification-driven and test-driven development practices.

## Skills

Development workflow skills are available to guide common tasks:

- **`spec-test-driven-development`**: Use when implementing new features or functionality. Provides complete workflow from specification through testing to implementation.

- **`specifying-requirements`**: Use when specifying a feature. Defines requirements as named, ignored Rust tests with the user story in the module doc.

- **`acceptance-test`**: Use when writing acceptance tests or scenarios. Defines Given/When/Then format and acceptance test patterns.

- **`test-driven-development`**: Use when writing tests. Defines RED-GREEN-REFACTOR cycle and test execution workflow. Includes language-specific guidance in PYTHON.md, RUST.md files.

- **`write-code`**: Use when implementing code to make failing tests pass. Defines the GREEN phase: minimal implementation, no untested features, and running the tests.

- **`prototyping`**: Use before writing code for a prototype. Defines the short path: the repo's existing language (Python, or TypeScript for frontend, when the repo shows no clear pattern), then the write-code skill, skipping specs, tests, and the rest of the workflow.

- **`refactoring-code`**: Use during REFACTOR phase of TDD (after GREEN), when logic is duplicated, or when locality of behavior is violated. Defines search-first workflow, duplication detection, locality principles, and safe refactoring practices.

- **`write-commit-message`**: Use when creating git commits. Defines conventional commit format and message structure guidelines.

- **`install-dependencies`**: Use when adding project dependencies. Defines dependency management rules and language-specific patterns for Python, Rust, and TypeScript.

- **`update-dependencies`**: Use when updating existing pinned dependencies. Defines unpin-resolve-repin workflow with test verification and rollback on failure.

- **`evaluation`**: Use when creating or updating agent evaluation suites. Defines eval structure, rubrics, and validation patterns.

- **`create-skill`**: Use when creating or modifying skills. Defines skill file structure, naming conventions, and integration patterns.

- **`pre-commit-hooks`**: Use when running pre-commit hooks manually. This project uses `prek`, not `pre-commit`. Defines correct commands for running hooks.

- **`error-handling`**: Use when writing, reviewing, or refactoring a try/except (or edge-case branch). Defines when to add a handler, when to remove one, and how to justify keeping it.
