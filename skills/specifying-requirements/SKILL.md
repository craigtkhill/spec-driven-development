---
name: specifying-requirements
description: Use when specifying a feature or adding requirements. Defines requirements as named, ignored Rust tests with the user story in the module doc.
---

# Specification Writing Skill

This skill defines how to write specifications that follow the project's conventions.
**The tests are the spec.** There is no separate spec file. A requirement is a test name.
**CRITICAL:** Stick to the Domain Specific Language in this document. Do not add your own extra keys or structure.

## Before Writing a Spec

**CRITICAL — before adding any requirements:**

1. **Check for conflicting specs** — read the existing tests in the same feature area to avoid overlap
2. **Check for duplicated requirements** — if a test already covers the behavior (even worded differently), do not add another
3. **Update the existing feature's tests first** if they already cover this feature

## Specification Location

**Specifications live close to the code** following the principle of locality of behavior:

- Location: In the same file as the code it specifies, in the test module ABOVE the implementation
- One feature = one test module
- End-to-end scenarios live in `tests/{feature}_scenarios.rs` (see the `acceptance-test` skill)

## Specification Format

Every feature must follow this structure:

```rust
//! Feature: Brief Feature Title
//!   user: user role
//!   goal: goal/capability
//!   solutions:
//!     - Solution 1
//!     - Solution 2

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_should_expected_behavior() { /* real test */ }

    #[test]
    #[ignore = "to-implement"]
    fn test_should_another_expected_behavior() {}
}
```

### Feature Section

The `//!` module doc captures the user story and possible solutions.

- `name`: Brief title for the feature
- `user`: The end user role (always from the user's perspective, never a system component)
- `goal`: The goal or capability (what they want)
- `solutions`: List of possible implementation approaches

**Rationale for User Goals + Possible Solutions:**
- Focus on WHAT the user wants to achieve, not a specific HOW
- Acknowledge that multiple solutions may exist to meet the user's goal
- Solutions should be considered throughout implementation
- Design the codebase to be modular enough to swap solutions without major refactoring
- Keeps options open until implementation details are needed

### Requirements Section

**Status comes from the test itself:**
- No test exists = not specified yet
- `#[ignore = "to-implement"]` = specified, not built
- `#[ignore = "wont-implement: <reason>"]` = intentionally not built
- Test passes = done

List the backlog with `cargo nextest run --run-ignored ignored-only`.

**Write ALL requirement stubs first** (empty `#[ignore = "to-implement"]` tests), then fill them in one at a time. A requirement with no stub is invisible.

**Requirements are a flat list — do NOT nest or group them.** Grouping by category creates artificial structure that encourages duplication.

**Requirement naming:**
- The test name IS the requirement: `test_should_{expected_behavior}`
- There are no requirement IDs
- Keep requirements atomic and testable
- One requirement per test
- Add a `///` line above a test only when its name is not enough

**CRITICAL - Atomic Requirements:**
- Each requirement must test ONE specific thing
- If a requirement has "and" or lists multiple attributes, split it into separate requirements
- Each requirement is one test

**CRITICAL - User-Facing Requirements Only:**
- Requirements must describe FEATURES from the user's perspective
- Each requirement should be stated ONLY ONCE in the tests
- DO NOT create separate requirements for implementation details

**CRITICAL - No Implementation Details in Requirements:**
- Requirements must describe WHAT the system does, never HOW it does it
- DO NOT name specific libraries, frameworks, or tools in requirements
- Library/tool choices belong in the `solutions` list, not in test names
- A requirement should remain valid even if the underlying implementation is swapped

**CRITICAL - Do Not Duplicate Existing Functionality:**
- Before writing any requirement, check whether the behavior is already implemented and tested in an existing module
- If the feature reuses existing infrastructure do NOT add requirements for that infrastructure
- Only specify behavior that is NEW to this feature

**Before adding a requirement, ask:**
1. Is this something the user directly experiences or cares about?
2. Have I already stated this requirement elsewhere in this feature's tests or in another test module?
3. Is this describing WHAT the system does for the user, or HOW it does it internally?
4. Is this behavior already implemented and tested in an existing module that this feature will reuse?

### Examples (Optional, Specification by Example)

A requirement can carry examples — concrete input/output pairs inside the test, as a loop over a table, that make an ambiguous rule unambiguous.

```rust
#[test]
fn test_should_expected_behavior() {
    for (input, expected) in [(input_1, output_1), (input_2, output_2)] {
        assert_eq!(function_under_test(input), expected, "{input:?}");
    }
}
```

- Only add examples when the test name alone leaves a case open to interpretation (e.g. boundary values, edge cases)
- Each example is a concrete case, not a restatement of the name
- Keep inputs and outputs flat — no nested implementation objects
- Not every requirement needs examples; skip them when the name is already unambiguous

### Scenarios (Optional)

**Use the `acceptance-test` skill for writing scenarios and acceptance tests.**

Scenarios are only needed when the feature requires end-to-end testing across multiple modules. Ask the user if scenarios apply before adding them.

## Integration with SDD Workflow

This spec skill is **STEP 1** of the spec-driven development workflow:

1. **Write Spec** ← (this skill): module doc + ignored stubs
2. Write Tests (remove `#[ignore]` and fill in each stub)
3. Implement Code (to pass tests)

After completing the spec:
1. Proceed to filling in the stubs using TDD. Do not wait for user approval.
2. Follow sdd skill for remaining steps
