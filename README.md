# Spec-Driven Development

```
   _____ ____  ____
  / ___// __ \/ __ \
  \__ \/ / / / / / /
 ___/ / /_/ / /_/ /
/____/_____/_____/

          Spec-Driven Development
```

**Agents and configs following a Spec-Driven Development process**

This repository is designed for **agent harnesses** like:
- **Claude Code**
- **Codex**
- **OpenCode**
- **Pi**


Spec-Driven Development provides a structured workflow for developing applications using agent harnesses, emphasizing specification-first development with comprehensive testing to ensure stability while moving with higher velocity.

*Note.* The aspiration is to make this toolkit agent harness agnostic. However, it is currently heavily configured for Claude Code.

## Workflow

![Workflow](workflow.svg)

The diagram is generated from [`workflow.py`](skills/sdd/workflow.py):

```bash
uv run python -I skills/sdd/create_diagram.py skills/sdd/workflow.py workflow.svg
```

## Quick Start

### Installation

Choose your agent harness and follow the installation guide:

- **[Claude Code](docs/install/CLAUDE-CODE.md)** - Setup for Claude Code users
- **[Codex](docs/install/CODEX.md)** - Setup for Codex users
- **[OpenCode](docs/install/OPENCODE.md)** - Setup for OpenCode users
- **[Pi](docs/install/PI.md)** - Setup for Pi users
- **[Other Agents](docs/install/OTHER-AGENTS.md)** - Setup for other agent harnesses

### Install as Claude Code Plugin

```bash
/plugin marketplace add https://github.com/craigtkhill/spec-driven-development
/plugin install spec-driven-development@spec-driven-development
```
