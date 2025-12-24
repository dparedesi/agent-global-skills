# Agent Global Skills

Agent global skills available across all repositories.

## Quick Start

After cloning, run the setup script to create a symlink so the skills are accessible from `~/.claude/skills/`:

```bash
cd ~/.agent/skills
chmod +x setup.sh
./setup.sh
```

## What the setup does

The setup script creates a symbolic link:

```
~/.claude/skills/ → ~/.agent/skills/
```

This allows:
- **Single source of truth**: All skills live in `~/.agent/skills/`
- **Claude compatibility**: Skills remain accessible from `~/.claude/skills/` where Claude Code expects them

## Available Skills

- **skill-builder/** - Create and evaluate Agent skills
- **skills-index-updater/** - Regenerate the skill index

## Manual Setup (Alternative)

If you prefer to set up manually:

```bash
# Ensure .claude directory exists
mkdir -p ~/.claude

# Remove existing skills directory if needed
# rm -rf ~/.claude/skills

# Create symlink
ln -s ~/.agent/skills ~/.claude/skills
```
