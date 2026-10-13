---
name: write-commit-message
description: Use when creating git commits. Defines conventional commit format and message structure guidelines.
---

# Commit Message Guidelines

Guidelines for writing clear, consistent git commit messages.

## Conventional Commits Format

Use the conventional commits style:

```
<type>[optional scope]: <description>
```

**CRITICAL: Single-line only. Never add a body or footer.** The code and spec speak for themselves.

### Commit Types

- **feat:** New feature
- **fix:** Bug fix
- **test:** Adding or updating tests
- **docs:** Documentation changes
- **refactor:** Code refactoring (no functional changes)
- **style:** Code style changes (formatting, whitespace)
- **chore:** Maintenance tasks, dependencies
- **perf:** Performance improvements
- **ci:** CI/CD configuration changes
- **build:** Build system changes

Pick the type from what kind of file changed, not from the intent behind the change. Use `feat`/`fix` only for changes to code.

### Scope (Optional)

Add scope in parentheses to provide additional context. Use the narrowest name that identifies what changed. Prefer the specific file, module, or component over a parent folder that holds many of them.

### Breaking Changes

Indicate breaking changes with `!` after type/scope:

### Description Guidelines

- Use imperative mood ("add feature" not "added feature")
- Start with lowercase
- No period at the end
- Keep under 72 characters
- Be specific and descriptive

## No Body, No Footer

**Never add a commit body or footer.** Every commit must be a single line only.

Do NOT include AI attribution, co-authored-by lines, or any other footers.

## Before Committing

**CRITICAL — all of the following MUST be true before committing:**

1. All tests pass (GREEN)
2. Pre-commit hooks pass — run `prek run --all-files` and fix every issue
3. Check for remote updates: `git fetch`
4. Review your changes: `git status` and `git diff`
5. Stage relevant files: `git add <files>`
6. Write clear commit message

❌ **NEVER commit with failing tests**
❌ **NEVER commit without running pre-commit hooks**
❌ **NEVER commit half-finished work**

## When to Commit

Commit once per completed requirement in the STDD cycle:

```
spec written → tests RED → tests GREEN → hooks pass → COMMIT
```

- One commit per requirement (or tightly related group of requirements)
- Each commit must represent a complete, working state
- Do not batch multiple requirements into one commit

## Integration with STDD Workflow

When following the spec-test-driven development workflow:

1. Pick an ignored requirement test
2. Write test → see RED
3. Implement → see GREEN
4. Run ALL tests → all pass
5. Run `prek run --all-files` → all hooks pass
6. Commit with a single-line conventional commit message
7. Repeat for next requirement
