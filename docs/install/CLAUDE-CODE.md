# Claude Code Setup

Run all commands from your **project root**.

This setup will:
1. Clone Spec-Driven Development to `.claude/` directory, creating `.claude/AGENTS.md`
2. Create a symlink `CLAUDE.md` in the project root pointing to `.claude/AGENTS.md`
3. Claude Code will read `CLAUDE.md` and access the skills index

## Installation

```bash
# Add Spec-Driven Development as a submodule
git submodule add https://github.com/craigtkhill/spec-driven-development.git .claude

# Initialize the submodule
git submodule update --init --recursive

# Create symlink to submodule's AGENTS.md for Claude Code (from project root)
ln -s .claude/AGENTS.md CLAUDE.md
```

See [Update Instructions](../update/CLAUDE-CODE.md) for how to update Spec-Driven Development.
