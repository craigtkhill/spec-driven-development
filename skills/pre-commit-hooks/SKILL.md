---
name: pre-commit-hooks
description: Use when running pre-commit hooks manually (e.g. before committing or after implementing). This project uses prek, not pre-commit. Defines the correct commands for running hooks.
---

# Pre-Commit Hooks

This project uses **prek** as the pre-commit hook runner. Do NOT use `pre-commit run` — always use `prek run`.

## Running Hooks

Run all hooks across all files:

```sh
prek run --all-files
```

Run hooks on specific files:

```sh
prek run --files path/to/file.rs
```

Run hooks on files changed since last commit:

```sh
prek run --last-commit
```

## When to Run

Always run `prek run --all-files` after implementing code and before committing, as part of the SDD workflow:

1. Tests pass (GREEN)
2. **Run `prek run --all-files`** ← here
3. Fix any issues raised
4. Commit

## Installing Hooks

On a fresh checkout, install the git hooks with:

```sh
just setup
```

Which runs:

```sh
prek install
prek install --hook-type commit-msg
prek install --hook-type pre-push
```

## Language-Specific Hooks

- Rust: See [RUST.md](RUST.md) for Rust-specific hooks including test-first ordering enforcement

## Hook Stages

Hooks are split across two stages:

- **pre-commit** (`prek install`): formatting, linting, style checks — run on every commit
- **pre-push** (`prek install --hook-type pre-push`): heavier checks like `cargo deny` — run on push
