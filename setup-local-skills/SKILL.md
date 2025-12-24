---
name: setting-up-local-skills
description: Set up AI tool symlinks in a repository for multi-agent compatibility. Use when the user wants to set up skills for Gemini, Claude, or other AI tools, or when they mention "setup skills", "configure agents", or "link AGENTS.md".
---

# Local Skills Setup

Create symlinks so multiple AI tools can use the same skill definitions from `.agent/`.

## Quick Start

| Tool | Command |
|------|---------|
| **Gemini** | `setup gemini` |
| **Claude** | `setup claude` |
| **All tools** | `setup all` |

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

### 1. Validate Prerequisites

Before creating symlinks, verify:

```bash
# Check if AGENTS.md exists (source of truth)
ls -la AGENTS.md

# Check if .agent/ directory exists
ls -la .agent/
```

- [ ] `AGENTS.md` exists in repo root
- [ ] `.agent/` directory exists (create if needed)

> [!TIP]
> If `.agent/skills/` doesn't exist locally, the skill symlinks will point to the global `~/.agent/skills/` via AGENTS.md references.

---

### 2. Create Symlinks Based on Tool

#### For Gemini

```bash
# Create symlink
ln -s AGENTS.md GEMINI.md

# Verify
ls -la GEMINI.md
```

#### For Claude

```bash
# Create .claude directory
mkdir -p .claude

# Create settings symlink (if .agent/settings.json exists)
[ -f .agent/settings.json ] && ln -s ../.agent/settings.json .claude/settings.json

# Create skills symlink (if .agent/skills exists)
[ -d .agent/skills ] && ln -s ../.agent/skills .claude/skills

# Verify
ls -la .claude/
```

---

### 3. Update .gitignore

Add symlinks to `.gitignore` to avoid committing them:

```bash
# Check if entries already exist
grep -E "^GEMINI\.md$|^\.claude/?$" .gitignore

# Add missing entries
cat >> .gitignore << 'EOF'

# AI tool symlinks (source of truth is AGENTS.md and .agent/)
GEMINI.md
.claude/
EOF
```

> [!IMPORTANT]
> Always verify `.gitignore` was updated before committing. Symlinks should not be tracked.

---

### 4. Verify Setup

```bash
# Check all symlinks are valid
for f in GEMINI.md .claude/skills .claude/settings.json; do
    [ -L "$f" ] && echo "✓ $f -> $(readlink $f)" || [ ! -e "$f" ] || echo "✗ $f exists but is not a symlink"
done

# Check .gitignore
grep -E "GEMINI|\.claude" .gitignore
```

---

## Quality Rules

- **AGENTS.md is the source of truth** — Never edit symlinked files directly
- **Symlinks must be in .gitignore** — Keep repo clean, only track actual content
- **Use relative paths** — Symlinks should work regardless of absolute path
- **Confirm before overwriting** — Script shows existing content and asks for Y/N confirmation before removing

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "File exists" error | Target already exists | Check if it's a symlink first, backup if needed |
| Symlink broken after clone | Absolute path used | Recreate with relative path |
| Changes not syncing | Editing symlink, not source | Edit `AGENTS.md` or `.agent/` directly |
| Git tracking symlink | Missing .gitignore entry | Add entry to .gitignore |

---

## Example: Full Setup

```bash
# Setup all tools at once
mkdir -p .claude

# Create symlinks (safe - won't overwrite)
[ ! -e GEMINI.md ] && ln -s AGENTS.md GEMINI.md
[ -d .agent/skills ] && [ ! -e .claude/skills ] && ln -s ../.agent/skills .claude/skills
[ -f .agent/settings.json ] && [ ! -e .claude/settings.json ] && ln -s ../.agent/settings.json .claude/settings.json

# Update .gitignore if needed
grep -q "^GEMINI\.md$" .gitignore 2>/dev/null || echo "GEMINI.md" >> .gitignore
grep -q "^\.claude/?$" .gitignore 2>/dev/null || echo ".claude/" >> .gitignore

# Verify
echo "=== Symlinks ==="
ls -la GEMINI.md .claude/ 2>/dev/null
echo "=== .gitignore ==="
grep -E "GEMINI|\.claude" .gitignore
```
