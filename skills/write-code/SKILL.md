---
name: write-code
description: Use when implementing code to make failing tests pass. Defines the GREEN phase: minimal implementation, no untested features, and running the tests.
---

# Write Code

Write the code that makes failing tests pass. Run this skill after the `test-driven-development` skill has produced tests that fail (RED).

## GREEN: Write Minimal Implementation

Write the MINIMUM code to make the tests pass.

**Key principle**: Don't add features not yet tested. Don't over-engineer.

**Run the tests again:**
- Run the tests to verify they now pass
- Expected outcome: GREEN (tests pass)

Then run ALL tests in the project to verify nothing broke.

## Rules

- Write ONLY enough code to make the current test pass
- Don't add features not yet tested
- Don't over-engineer solutions
- Prefer simple over clever
- Reuse existing infrastructure where possible

## Common Mistakes to Avoid

### ❌ Over-Implementing
- Adding features not yet tested
- Writing more code than needed to pass the test
- Implementing based on assumptions rather than tests

## After GREEN

- Use the `refactoring-code` skill to clean up once all tests pass
