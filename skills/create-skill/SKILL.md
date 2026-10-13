---
name: create-skill
description: Use when creating or modifying skills. Defines skill file structure, naming conventions, and integration patterns.
---

# Creating Agent Skills

## Overview

Skills in for Agents provide reusable workflows and guidelines. This skill documents how to properly create new skills.

## Required File Structure

These skills are designed to be agent harness agnostic. They live in the dotfolders for the agentic application
examples include.
```
.claude/
.codex/
.opencode/
.pi/
```

Henceforth, we will use .harness/ as shorthand

Every skill must have:
```
.harness/skills/skill-name/
├── SKILL.md (REQUIRED - main skill file with frontmatter)
├── supporting-file.md (optional)
└── templates/ (optional)
```

## SKILL.md Requirements

### 1. YAML Frontmatter (REQUIRED)

Every SKILL.md **must** start with YAML frontmatter:

```yaml
---
name: skill-name
description: Brief description of what this skill does and when to use it
---
```

**Frontmatter Rules:**
- `name`: Lowercase letters, numbers, hyphens only (max 64 chars)
- `description`: Explain WHAT it does + WHEN to use it (max 1024 chars)
- Critical: agent harnesses use description for automatic skill discovery

### 2. Main Content

After frontmatter, elicit the human to add the skill instructions in markdown:


## Skill Naming Conventions

**DO:**
- ✅ Use lowercase letters
- ✅ Use hyphens for word separation
- ✅ Make names descriptive but concise
- ✅ Keep under 64 characters

**DON'T:**
- ❌ Use uppercase letters
- ❌ Use underscores
- ❌ Use spaces
- ❌ Use special characters

**Examples:**
- ✅ `create-skill`
- ✅ `test-driven-development`
- ✅ `write-commit-message`
- ❌ `Create_Skill`
- ❌ `test driven development`

## Description Best Practices

The description is **critical** for skill discovery and invocation.

**Purpose**: Help Claude decide whether to READ the skill, not to contain the rules themselves.

**Format**: "Use when [specific trigger]. Defines [what's inside]."

**Guidelines:**
1. **Start with trigger**: Begin with "Use when [action/situation]"
2. **Be concise**: Keep under 200 characters if possible
3. **Specific triggers**: Include clear conditions for when to invoke

## Supporting Files

Skills can include additional files referenced from SKILL.md:

```markdown
For Python, where it differs from the Rust approach: See [PYTHON.md](PYTHON.md)
```

**Common Supporting Files:**
- Guides for other languages where they differ from Rust (`PYTHON.md`, `TYPESCRIPT.md`)
- Templates (`TEMPLATE.md`, `templates/spec-template.md`)
- Examples (`EXAMPLES.md`)
- Scripts (`scripts/helper.py`)

Additionally register skills to the projects AGENTS.md file.

## Creation Checklist

When creating a new skill:

- [ ] Create directory: `.harness/skills/skill-name/`
- [ ] Create `SKILL.md` with YAML frontmatter
- [ ] Add `name` field (lowercase, hyphens, max 64 chars)
- [ ] Add `description` field (WHAT + WHEN, max 1024 chars)
- [ ] Ask human to add more details and and supporting files
- [ ] Reference supporting files with relative paths
- [ ] Test skill discovery with `/help`
- [ ] Regiser skill to AGENTS.md

## Allows follow these practices

✅ **Always include frontmatter** - SKILL.md must start with YAML frontmatter
✅ **Write clear descriptions** - Description must explain WHAT and WHEN
✅ **Use correct filename** - Must be `SKILL.md` (uppercase)
✅ **Use proper naming** - Use lowercase letters and hyphens for separation
✅ **Be specific** - Clearly define when to use the skill
✅ **Keep content project-agnostic** - Do not make guidelines specific to the current project; make SKILL.md and supporting files reusable across projects
✅ **Rust first** - Write SKILL.md for Rust: Rust code, commands, and examples belong in SKILL.md
✅ **Separate other languages** - Put details for another language in its own file (PYTHON.md, etc.) only where it differs from the Rust approach
✅ **Provide complete templates** - Include full templates, not partial ones
✅ **Prioritize clear descriptions** - Use examples only when necessary for clarity
✅ **Work in small steps** - Only implement what was requested, collaborate incrementally in small steps with the user
✅ **Use positive framing** - Describe what to do rather than what not to do when writing guidelines but use negatives when it provides extra clarity

## Skill Integration

Skills can reference other skills:

```markdown
**Use the `specifying-requirements` skill for writing specifications.**
**Use the `test-driven-development` skill for writing tests.**
```

This creates workflows that combine multiple skills.

## Testing Your Skill

After creating a skill:

1. Run `/help` to verify it's discovered
2. Check the description appears correctly
3. Test invoking the skill in context
4. Verify supporting files load correctly

## Reference

Official documentation: https://code.claude.com/docs/en/skills.md
