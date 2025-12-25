---
name: skills-local-setup
description: Set up AI tool symlinks in a repository for multi-agent compatibility. Use when the user wants to set up skills for Gemini, Claude, or other AI tools, or when they mention "setup skills", "configure agents", or "link AGENTS.md".
---

# Local Skills Setup

Create symlinks so multiple AI tools can use the same skill definitions from `.agent/`.

**Why?** Different AI tools look for config in different places (`.claude/`, `GEMINI.md`). This skill creates symlinks so you maintain ONE source of truth in `.agent/` and `AGENTS.md`.

## Quick Start

```bash
# Run from any repo root (script is in the global skill location)
~/.claude/skills/skills-local-setup/scripts/skills-local-setup.sh [gemini|claude|all]
```

---

## Supported Tools

| Tool | Symlink Created | Points To |
|------|-----------------|-----------|
| Gemini | `GEMINI.md` | `AGENTS.md` |
| Claude | `.claude/settings.json` | `.agent/settings.json` |
| Claude | `.claude/skills/` | `.agent/skills/` |

> [!NOTE]
> All symlinks are automatically added to `.gitignore` to keep the repo clean.

---

## Workflow

### 1. Run the Setup Script

```bash
# From repo root — script lives in the global skills directory
~/.claude/skills/skills-local-setup/scripts/skills-local-setup.sh [gemini|claude|all]
```

The script automatically:
- Validates prerequisites (git repo)
- Creates `.agent/skills/` directory if it doesn't exist
- Creates symlinks with relative paths
- Safely adds entries to `.gitignore` (handles missing newlines)
- Asks for Y/N confirmation before overwriting existing files

> [!TIP]
> If `AGENTS.md` doesn't exist when setting up Gemini, the script will instruct you to run the `skills-index-updater` skill first to create it.


---

### 2. Verify Setup

```bash
# Check symlinks are valid
ls -la GEMINI.md .claude/ 2>/dev/null

# Check .gitignore
grep -E "GEMINI|\.claude" .gitignore

# Check git status (symlinks should be ignored)
git status
```

---

## Quality Rules

- **AGENTS.md is the source of truth** — Never edit symlinked files directly
- **Symlinks must be in .gitignore** — Keep repo clean, only track actual content
- **Use relative paths** — Symlinks should work regardless of absolute path
- **Confirm before overwriting** — Script shows existing content and asks for Y/N confirmation before removing

### Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Use absolute paths in symlinks | Breaks when repo moves or on other machines | Use relative paths (`../`) |
| Commit symlinks to git | Creates merge conflicts, breaks for others | Add to `.gitignore` |
| Edit GEMINI.md or .claude/ directly | Changes won't sync to other tools | Edit `AGENTS.md` or `.agent/` |
| Run outside repo root | Symlinks will be created in wrong location | `cd` to repo root first |

### Validation Checklist

Before considering setup complete:
- [ ] `ls -la` shows symlinks pointing to correct targets
- [ ] `git status` shows no untracked symlinks
- [ ] `.gitignore` contains entries for all symlinks

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "File exists" error | Target already exists | Check if it's a symlink first, backup if needed |
| Symlink broken after clone | Absolute path used | Recreate with relative path |
| Changes not syncing | Editing symlink, not source | Edit `AGENTS.md` or `.agent/` directly |
| Git tracking symlink | Missing .gitignore entry | Add entry to .gitignore |
| AGENTS.md not found | Missing AGENTS.md file | Run `/skills-index-updater` skill first |

