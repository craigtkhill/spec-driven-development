# Generic Agent Harness Setup

This guide covers the general pattern for setting up Spec-Driven Development with any agent harness that isn't specifically documented.

## Installation Pattern

Most agent harnesses follow this pattern for project-specific configuration:

```bash
# 1. Add Spec-Driven Development as a git submodule in your agent harness's config directory
git submodule add https://github.com/craigtkhill/spec-driven-development.git .<harness-name>

# 2. Initialize the submodule
git submodule update --init --recursive
```

Replace `<harness-name>` with your agent harness's config directory name (e.g., `claude`, `cursor`, `codex`).

## Discovery Mechanisms

Different agent harnesses discover skills in different ways:

### AGENTS.md-based (Claude Code, Codex, Pi)
If your agent harness reads from `AGENTS.md` or a specific config file:

```bash
# Create a symlink in project root to the submodule's AGENTS.md
ln -s .<harness-name>/AGENTS.md <CONFIG-FILE>.md
```

### Directory scanning (OpenCode)
If your agent harness automatically scans subdirectories for skills, the submodule at `.<harness-name>/` will work directly.

### Custom config files
If your agent harness uses a different config file name (e.g., CURSOR.md):

```bash
# Create a symlink in project root to the submodule's AGENTS.md
ln -s .<harness-name>/AGENTS.md <YOUR-CONFIG-FILE>.md
```

See [Update Instructions](../update/OTHER-AGENTS.md) for how to update Spec-Driven Development.

## Next Steps

Check your agent harness's documentation to understand:
1. Where its configuration directory is located
2. How it discovers agent skills or instructions
3. Whether it uses AGENTS.md or a different file format
