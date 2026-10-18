---
name: test-driven-development
description: Use when writing tests. Defines RED-GREEN-REFACTOR cycle and test execution workflow; the GREEN implementation lives in the write-code skill.
---

# Test-Driven Development (TDD) Skill

This skill defines the proper TDD workflow: write test(s), run them (RED), implement minimal code (GREEN), run ALL tests (VERIFY), repeat.

**Language-specific details**:
- For Python projects: See `test-driven-development/PYTHON.md` for pytest patterns, running tests, and Python-specific examples
- Other languages: Add new files to `test-driven-development/` directory as needed

## TDD Cycle: RED → GREEN → REFACTOR

### How Many Tests to Write at Once?

**Write ONE test at a time when:**
- Design is uncertain or exploratory
- Domain is complex and unfamiliar
- You need to review and course correct after each step
- Implementation approach is unclear

**Write MULTIPLE tests upfront when:**
- Requirements are clear and well-understood
- Domain is familiar
- Design is straightforward
- You're confident in the implementation approach

### 1. RED: Write Failing Test(s)

Write test(s) that fail.

**Key principle**: Each test must fail for the right reason (missing implementation, not syntax error).

**CRITICAL - Run the tests - they MUST fail:**
- ❌ DO NOT write implementation before running the tests
- ❌ DO NOT skip the RED phase
- ✅ DO run the tests to verify they fail
- Verify they fail with expected error (import error, assertion failure, etc.)
- Expected outcome: RED (tests fail)

**Why RED is mandatory:**
- Confirms the tests actually test something
- Prevents false positives (tests that always pass)
- Validates test setup is correct

### 2. GREEN: Write Minimal Implementation

**Use the `write-code` skill to write the minimal implementation and run the tests until they pass.**

### 3. VERIFY: Run ALL Tests

**CRITICAL**: After tests pass, run ALL tests to ensure nothing broke.

**Key principle**: Never break existing functionality.

**Run complete test suite:**
- Run all tests in the project
- Verify all tests pass (new and existing)
- Expected outcome: All tests GREEN

### 4. REFACTOR: Improve Code Quality

After tests pass, consider refactoring to improve code quality.

**Use the `refactoring-code` skill for detailed refactoring guidance.**

**Key principle**: Refactor only when tests are GREEN. Tests protect you during refactoring.

**When to refactor:**
- Code duplication exists
- Code is unclear or hard to understand
- Better patterns or abstractions are apparent
- Performance can be improved
- Before implementing new features that may duplicate existing patterns

**Refactoring safety:**
- Run ALL tests after each refactoring change
- If any test fails, revert and try a different approach
- Keep refactoring changes small and incremental

**Note**: Refactoring is optional on each cycle. You can skip if code is already clean.

### 5. REPEAT: Continue

After all tests pass, continue with next requirements and repeat the cycle.

## TDD Rules

### Rule 1: The Tests Are the Spec
- ✅ DO start from an `#[ignore = "to-implement"]` stub and remove `#[ignore]` when you write the test
- ✅ DO keep test names accurate; renaming a test changes the spec
- No markers to update: passing = done, ignored = not built

### Rule 2: Always Run Tests
**CRITICAL**: Tests MUST go through the RED → GREEN → VERIFY cycle:
1. **RED**: Run tests to see them FAIL (before implementing)
2. **GREEN**: Run tests to see them PASS (after implementing)
3. **VERIFY**: Run **ALL tests** in the project to verify nothing broke

❌ **NEVER skip the RED phase** - Always see tests fail before implementing

**Why this matters:**
- RED phase confirms tests actually test something (prevents false positives)
- GREEN phase confirms implementation works
- VERIFY phase ensures no regression in existing functionality

### Rule 3: Minimal Implementation
- Use the `write-code` skill; it writes ONLY enough code to make the current test pass

### Rule 4: Test One Thing
- Each test validates ONE behavior
- One assertion per test (unless assertions are intrinsically coupled)
- Clear test names describe what's being tested
- Multiple tests enable better parallelization

### Rule 5: Fail Fast
If all tests don't pass:
- Stop immediately
- Fix the broken tests
- Don't continue until all tests GREEN

## TDD Workflow Diagram

See [WORKFLOW.md](WORKFLOW.md) for the full step-by-step diagram.

## Test Organization

### Unit Tests

- Test individual functions/classes in isolation
- Fast, focused, and run frequently
- Located within the feature directory
- Should cover the vast majority of your testing needs

**For acceptance tests and scenarios, use the `acceptance-test` skill.**

### Test Grouping
Organize tests by feature:
- Group related tests together
- Use clear section/class names

### Test Naming
Follow project conventions for test names:
- Descriptive names that explain what's being tested
- The name IS the requirement; add a `///` line only if the name is not enough
- Use consistent naming pattern

### Test Documentation
Each test should have:
- Clear name describing behavior

## Integration with STDD Workflow

TDD is **STEP 2** of the spec-test-driven development workflow:

1. Write Spec (use `spec` skill)
2. **Write Tests** ← (use this `tdd` skill)
3. Implement Code (use the `write-code` skill)

When writing tests:
1. Start from the ignored stubs written in the spec step
2. Fill in one stub at a time
3. Write tests for every stub
4. Decide whether to write one test at a time or multiple tests based on complexity and certainty (see "How Many Tests to Write at Once?" above)

## Common Mistakes to Avoid

### ❌ Not Running Tests Enough
- Skipping the RED phase (not verifying test fails)
- Skipping the GREEN phase (not verifying test passes)
- Skipping the VERIFY phase (not running all tests)

### ❌ Writing Bad Tests
- Tests that don't fail when they should
- Tests with multiple assertions (unless intrinsically coupled)
- Tests that don't clearly document what they're testing
- Using mocks — always use real implementations instead of mocks

## Checklist Before Moving Forward

Use this checklist for your TDD workflow **in this exact order**:

1. [ ] Tests written with clear names and documentation
2. [ ] Each test started from an ignored requirement stub
3. [ ] **Tests run and FAILED (RED)** ✓ ← DO NOT SKIP THIS
4. [ ] Minimal implementation written (ONLY after seeing RED)
5. [ ] Tests run and PASSED (GREEN) ✓
6. [ ] ALL tests run and PASSED (VERIFY) ✓
7. [ ] `#[ignore]` removed from the tests now passing
8. [ ] Code refactored if needed (optional)
9. [ ] ALL tests still pass after refactoring
10. [ ] No broken tests
11. [ ] Ready to continue

**Critical reminder:** Steps 3-6 MUST happen in order:
- RED (tests fail) → then implement → GREEN (tests pass) → then VERIFY (all tests pass)

