---
name: acceptance-test
description: Use when writing acceptance tests or scenarios. Defines Given/When/Then format and acceptance test patterns.
---

# Acceptance Test Skill

This skill defines how to write acceptance tests and scenarios that validate end-to-end feature behavior.

## When to Write Acceptance Tests

Write acceptance tests when the feature requires end-to-end testing across multiple modules or external dependencies.

- Testing complete user workflows that involve external APIs, databases, or services
- Verifying business requirements are satisfied across module boundaries
- Testing features that span multiple units within the feature
- When a test requires mocking dependencies, it should be an acceptance test

If the feature only involves isolated logic within a single module, use unit tests instead.

## Scenarios

Scenarios are acceptance tests in `tests/{feature}_scenarios.rs`. Only add them when the feature requires end-to-end testing with other modules. Ask the user if scenarios apply before adding them.

```rust
/// Scenario: Descriptive scenario name
#[test]
#[ignore = "to-implement"]
fn descriptive_scenario_name() {
    // given: setup/preconditions
    // when: user action/trigger
    // then: expected outcome/verification
}
```

Write the ignored stub first, then fill it in.

**Describe WHAT, not HOW:**
- Focus on user behavior and system outcomes
- Avoid implementation details (field names, status codes, internal states)
- Describe the value and intent, not the mechanics
- Keep scenarios at a high level of abstraction

**Cover end-to-end flows:**
- Start with user perspective
- Verify final state

## Acceptance Test Structure

Acceptance tests follow the Given/When/Then pattern:

- **Given** — Setup/preconditions
- **When** — User action/trigger
- **Then** — Expected outcome/verification

Each acceptance test is one scenario.

## Acceptance Tests vs Unit Tests vs Integration Tests

**Unit Tests:**
- Test individual functions/classes in isolation
- Fast, focused, and run frequently
- Live in the `tests` module next to the code

**Acceptance Tests:**
- Test complete features from a user/business perspective
- Verify requirements are met end-to-end within a feature
- Test scenarios (Given/When/Then)
- May involve multiple units working together
- Live in `tests/{feature}_scenarios.rs`

**Integration Tests:**
- Test interactions between multiple modules or external systems
- Use sparingly and only for tactical purposes
- Located in `tests/` directory at project root

**Test hierarchy:** Default to unit tests. Use acceptance tests when you need end-to-end feature validation. Use integration tests sparingly for tactical external integration needs.
