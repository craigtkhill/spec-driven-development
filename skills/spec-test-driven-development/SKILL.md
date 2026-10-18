---
name: spec-test-driven-development
description: Defines complete workflow from specification through testing to implementation.
---


The workflow is defined as code in [workflow.py](workflow.py).

## Workflow Steps

### 0. Update Dependencies FIRST
**Use the `update-dependencies` skill to update all dependencies before starting any new feature.**

- Run before writing the spec for any new feature cycle
- Ensures you build on up-to-date, secure dependencies
- If updates cause test failures, resolve them before proceeding

### 1. Write Specification FIRST (ignored test stubs)
**Use the `specifying-requirements` skill. The tests are the spec; there is no spec file.**

- Feature story goes in the `//!` module doc
- Each requirement is an empty `#[ignore = "to-implement"]` test named `test_should_...`

After writing the stubs:
- Proceed straight to tests. Do not stop for user approval.
- Tell the user which file holds the spec, then keep working.

### 2. Write Tests SECOND (before implementation)
- Remove `#[ignore]` and fill in one stub at a time
- One assertion per test (performance costs permitting)
- Test naming: `test_should_{expected_behavior}`
- Unit tests live in the test module above the implementation

**When to write unit tests vs acceptance tests:**
- **Unit tests**: For isolated logic that doesn't require mocking
- **Acceptance tests**: Use the `acceptance-test` skill for guidance on when and how to write acceptance tests

### 3. Implement Code LAST
- Write minimal code to make tests pass
- Reuse existing infrastructure where possible
- Update todo list as you work
- Status needs no bookkeeping: a passing test means done, `#[ignore]` means not built

### 4. Run Tests to Verify Implementation
- **CRITICAL: After completing implementation, ALWAYS run the tests**
- All tests must pass before marking work as complete
- If tests fail, fix the implementation and re-run until all tests pass
- **DO NOT claim work is complete without running and passing tests**

**Use the `test-driven-development` skill for language-specific test running instructions:**
- The TDD skill contains detailed patterns for running tests
- For other languages: See corresponding files in `test-driven-development/{language}.md`

### 5. Run Pre-commit Hooks Before Completion
- **CRITICAL: After tests pass, ALWAYS run pre-commit hooks**
- Pre-commit hooks run linters, formatters, and static analysis tools
- Fix any issues raised by pre-commit hooks before marking work as complete
- **DO NOT claim work is complete without running and passing pre-commit hooks**

**Run pre-commit hooks:**
```bash
prek run --all-files
```

## Commit Workflow

**Use the `write-commit-message` skill for git commit guidelines.**

## Do NOT Proceed Without

1. ❌ Do NOT write implementation code before updating dependencies
2. ❌ Do NOT write implementation code before spec
3. ❌ Do NOT write implementation code before tests
4. ❌ Do NOT skip writing tests
5. ❌ Do NOT write multiple assertions per test (unless justified)
6. ❌ Do NOT skip running tests after implementation
7. ❌ Do NOT skip running pre-commit hooks before completion
8. ✅ DO update dependencies → write spec → tests → implementation → run tests → run pre-commit in that order
9. ✅ DO continue from spec to tests without waiting for user approval
10. ✅ DO use TodoWrite to track progress
11. ✅ DO run tests and verify all pass
12. ✅ DO run pre-commit hooks and fix all issues