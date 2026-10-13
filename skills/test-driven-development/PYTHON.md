# TDD for Python

Python-specific patterns and conventions for Test-Driven Development.

## Test File Location

### Unit Tests
Unit tests go in `test.py` within the feature directory (NOT in a separate `tests/` directory).

### Integration Tests
Integration tests go in the `tests/` directory at the project root.

**When to write integration tests:**
- Testing interactions between multiple modules
- **Tactical purposes only** - integration tests are expensive to run and maintain
- Only add integration tests when unit tests cannot adequately verify the behavior

**Integration test structure:**
```
tests/
  __init__.py
  test_feature_integration.py
```

## Test Framework: pytest

Use **pytest** with the following conventions:

### Test Class Organization

Organize tests by requirement sections using classes:

### Test Naming Convention

Follow this pattern:

```python
def test_should_{expected_behavior}(self) -> None:
    """Requirement description"""
    # Given
    # When
    # Then - ONE assertion only
```

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
```python
def test_should_parse_and_validate_complex_structure(self) -> None:
    """When all assertions verify aspects of one indivisible outcome."""
    result = parse_complex_data(input)
    # These assertions all verify the same conceptual outcome
    assert result.is_valid
    assert result.error_count == 0
    assert result.data is not None
```

**When tests are expensive (DB, APIs, slow setup):**
- Don't use multiple assertions to optimize
- Instead, write **acceptance tests** (not unit tests)
- Acceptance tests are designed for integration/expensive operations

**Default rule**: Write one assert per test unless assertions are intrinsically coupled.

### Required Imports

Common imports for tests:

```python
from uuid import uuid4

import pytest
from pydantic import ValidationError
```

## Running Tests with pytest and uv

Use `uv` as the package manager.

### Run single test (during TDD RED/GREEN phases):
```bash
uv run pytest src/module/feature/test.py::TestClass::test_name -v
```

### Run all tests in a feature:
```bash
uv run pytest src/module/feature/test.py -v
```

### Run ALL tests (VERIFY phase):
```bash
uv run pytest -v
```

### Run with coverage:
```bash
uv run pytest --cov=src --cov-report=term-missing -v
```

### One Assert Per Test

```python
# ✓ Correct - one assertion per test
def test_should_have_minimum_value_1(self) -> None:
    assert Model.model_fields['count'].ge == 1

def test_should_have_maximum_value_8(self) -> None:
    assert Model.model_fields['count'].le == 8

# ✗ Avoid - multiple assertions (unless performance critical)
def test_count_constraints(self) -> None:
    assert Model.model_fields['count'].ge == 1
    assert Model.model_fields['count'].le == 8
```

## Debugging Failed Tests

### View detailed error:
```bash
uv run pytest src/module/test.py::test_name -v --tb=short
```

### Drop into debugger on failure:
```bash
uv run pytest src/module/test.py::test_name --pdb
```

### Show print statements:
```bash
uv run pytest src/module/test.py::test_name -v -s
```

## Test Configuration

Tests are configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests", "src"]  # Look for tests in both locations
python_files = ["test_*.py", "test.py"]
python_functions = ["test_*"]
asyncio_mode = "auto"
addopts = "-v --strict-markers --strict-config --cov=src --cov-report=term-missing --cov-branch"
```

## Common Errors and Solutions

### ModuleNotFoundError: No module named 'src'
**Solution**: Ensure `__init__.py` exists in all parent directories:

```bash
touch src/__init__.py
touch src/module/__init__.py
touch src/module/feature/__init__.py
```

### ImportError in test.py
**Solution**: Use absolute imports from project root:

```python
# ✓ Correct
from src.module.feature.model import MyModel

# ✗ Wrong
from model import MyModel
```

### Test not discovered
**Solution**: Ensure test file is named `test.py` or `test_*.py` and functions start with `test_`

## Coverage Goals

This project aims for 100% test coverage. Check coverage with:

```bash
uv run pytest --cov=src --cov-report=term-missing -v
```

Coverage is shown after test run. Ensure new code has 100% coverage.
