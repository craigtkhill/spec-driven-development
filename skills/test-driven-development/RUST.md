# TDD for Rust

Rust-specific patterns and conventions for Test-Driven Development.

## Test File Location

### Unit Tests
**CRITICAL**: Unit tests MUST be in the same file as the implementation code.

**CRITICAL**: Unit tests MUST be placed ABOVE the implementation code in the file.

```rust
// src/feature/models.rs

// ============================================
// TESTS
// ============================================
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_should_do_something() {
        // Test implementation
    }
}

// ============================================
// IMPLEMENTATION
// ============================================
pub struct Model {
    data: Vec<String>,
}

impl Model {
    pub fn new(data: Vec<String>) -> Result<Self, String> {
        // Implementation
    }
}
```

**File structure:**
```
src/
  feature/
    mod.rs          # Feature module exports
    models.rs       # //! feature story, tests ABOVE implementation
```

### Integration Tests
Integration tests go in the `tests/` directory at the project root.

**When to write integration tests:**
- Testing interactions between multiple modules/features
- **Tactical purposes only** - integration tests are expensive to run and maintain
- Only add integration tests when unit tests cannot adequately verify the behavior
- Testing with external dependencies (file system, network, LLMs)

**Integration test structure:**
```
tests/
  feature_integration.rs
  common/
    mod.rs          # Shared test utilities
```

## Test Framework: Built-in Rust Testing

Use Rust's built-in **test framework** with the following conventions:

### Test Module Organization

Organize tests by feature area using modules:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    // Validation tests
    mod validation {
        use super::*;

        #[test]
        fn test_should_validate_required_field() {
            // Test implementation
        }
    }

    // Business logic tests
    mod business_logic {
        use super::*;

        #[test]
        fn test_should_process_data() {
            // Test implementation
        }
    }
}
```

### Test Naming Convention

Follow this pattern:

```rust
#[test]
fn test_should_{expected_behavior}() {
    // Given

    // When

    // Then - ONE assertion only
}
```

**Requirements:**
- The test name IS the requirement; there are no requirement IDs
- Add a `///` line above the test only when the name is not enough
- Unwritten requirements are empty stubs: `#[test] #[ignore = "to-implement"] fn test_should_...() {}`
- List the backlog with `cargo nextest run --run-ignored ignored-only`

**Given/When/Then Comments:**
- Use simple comments: `// Given`, `// When`, `// Then`
- DO NOT add extra details or descriptions after these labels
- The code itself should be self-documenting

**CRITICAL: One Assert Per Test**

Each test must have exactly ONE assertion. This ensures:
- Clear test failure messages
- Easy to identify what broke
- Tests validate one specific behavior
- Better test organization
- Better parallelization

**Exception: Multiple assertions only when:**
- Testing intrinsically coupled behavior that cannot logically be separated
  - Every effort must be made to decouple it first however.
- The assertions verify different aspects of a single, indivisible outcome

**Example of acceptable multiple assertions:**
```rust
#[test]
fn test_should_parse_and_validate_complex_structure() {
    // When all assertions verify aspects of one indivisible outcome
    let result = parse_complex_data(input);

    // These assertions all verify the same conceptual outcome
    assert!(result.is_valid);
    assert_eq!(result.error_count, 0);
    assert!(result.data.is_some());
}
```

**When tests are expensive (IO, network, slow setup):**
- Don't use multiple assertions to optimize
- Instead, write **acceptance tests** (not unit tests)
- Acceptance tests are designed for integration/expensive operations

**Default rule**: Write one assert per test unless assertions are intrinsically coupled.

## Running Tests with Nextest

Use `cargo` as the build tool and `cargo-nextest` as the test runner (`cargo install cargo-nextest`). Nextest runs tests in a separate process per test and is significantly faster than `cargo test` on multi-test suites.

### Run single test (during TDD RED/GREEN phases):
```bash
cargo nextest run -E 'test(test_should_validate_input)'
```

### Run all tests matching a pattern:
```bash
cargo nextest run validation
```

### Run all tests in a module:
```bash
cargo nextest run feature::tests
```

### Run ALL tests (VERIFY phase):
```bash
cargo nextest run
```

### Run tests with output (show println! statements, even on pass):
```bash
cargo nextest run --no-capture
```

### Run integration tests only:
```bash
cargo nextest run --test '*'
```

### Run with specific number of threads:
```bash
cargo nextest run --test-threads=1  # Sequential
cargo nextest run --test-threads=4  # Parallel with 4 threads
```

### Doctests
Nextest does not run doctests. Run them separately:
```bash
cargo test --doc
```

## Test Organization Patterns

### Standard Pattern: Tests Above Implementation
**CRITICAL**: Tests MUST be placed ABOVE implementation in the same file.

**For files with structs, enums, and impl blocks, the order MUST be:**
1. Imports
2. Tests (#[cfg(test)] mod tests { ... })
3. Type definitions (structs, enums - declarations only)
4. Implementation (impl blocks, Default implementations, methods)
5. Public functions

**Rationale:**
- Tests define the API contract first (TDD principle)
- You see what needs to be implemented before writing it
- Tests use `use super::*;` to access types defined later in file
- Rust resolves all definitions in module scope, so this works perfectly

```rust
// src/feature/models.rs

// 1. Imports
use anyhow::Result;
use std::path::Path;

// 2. TESTS (FIRST!)
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_should_validate_input() {
        // Given
        let input = vec!["test".to_string()];

        // When
        let result = Model::new(input);

        // Then
        assert!(result.is_err());
    }
}

// 3. Type Definitions
pub struct Model {
    field: String,
}

pub enum Status {
    Active,
    Inactive,
}

// 4. Implementations
impl Model {
    pub fn new(field: String) -> Result<Self, String> {
        // implementation
    }
}

impl Default for Status {
    fn default() -> Self {
        Self::Active
    }
}

// 5. Public Functions
pub fn process_model(model: Model) -> Result<()> {
    // implementation
}
```

**Why tests go above implementation:**
- Tests define the interface first (TDD principle)
- See failing tests before writing implementation
- Tests document expected behavior at the top
- Implementation follows the contract defined by tests

## One Assert Per Test Examples

```rust
// ✓ Correct - one assertion per test
#[test]
fn test_should_have_minimum_value() {
    let model = create_test_model();
    assert_eq!(model.min(), 1);
}

#[test]
fn test_should_have_maximum_value() {
    let model = create_test_model();
    assert_eq!(model.max(), 100);
}

// ✗ Avoid - multiple assertions (unless intrinsically coupled)
#[test]
fn test_model_constraints() {
    let model = create_test_model();
    assert_eq!(model.min(), 1);   // Split into separate tests
    assert_eq!(model.max(), 100);
}
```

## Debugging Failed Tests

### View detailed error with backtrace:
```bash
RUST_BACKTRACE=1 cargo nextest run test_name
```

### Run test with full backtrace:
```bash
RUST_BACKTRACE=full cargo nextest run test_name
```

### Run ignored tests:
```bash
cargo nextest run --run-ignored ignored-only
```

### Run specific test with verbose output:
```bash
cargo nextest run --no-capture -E 'test(test_name)'
```

## Test Configuration

Tests are configured in `Cargo.toml`:

```toml
[dev-dependencies]
# Add test-only dependencies here

[[test]]
name = "integration_test"
path = "tests/integration_test.rs"

[profile.test]
opt-level = 0  # No optimization for faster compilation
```

## Coverage Tools

Rust test coverage can be measured using:

### Using cargo-tarpaulin (Linux/WSL)
```bash
# Install
cargo install cargo-tarpaulin

# Run coverage
cargo tarpaulin --out Html --output-dir coverage
```

### Using cargo-llvm-cov (All platforms)
```bash
# Install
cargo install cargo-llvm-cov

# Run coverage
cargo llvm-cov --html

# Run coverage with output
cargo llvm-cov --open
```

## Test Helpers and Fixtures

```rust
#[cfg(test)]
mod tests {
    use super::*;

    // Helper function for test setup
    fn create_test_data() -> Vec<String> {
        vec![
            "item1".to_string(),
            "item2".to_string(),
            // ... more items
        ]
    }

    // Setup and teardown pattern
    fn setup() -> TestContext {
        TestContext::new()
    }

    #[test]
    fn test_with_helper() {
        let context = setup();
        // test using context
    }
}
```

## Coverage Goals

This project aims for high test coverage (ideally 100%). Check coverage with:

```bash
cargo llvm-cov
```

Ensure new code has comprehensive test coverage before marking features complete.
