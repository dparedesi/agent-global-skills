# Claude Global Skills

Global skills available across all repositories.

## Quick Start

After cloning/moving to `~/.claude/skills/`, run the setup script to create a backward-compatible symlink at `~/.agent/skills/`:

```bash
cd ~/.claude/skills
chmod +x setup.sh
./setup.sh
```

## What the setup does

The setup script creates a symbolic link:

```
~/.agent/skills/ → ~/.claude/skills/
```

This allows:
- **Single source of truth**: All skills live in `~/.claude/skills/`
- **Backward compatibility**: Skills remain accessible from `~/.agent/skills/` for older configurations

## Available Skills

- **skill-builder/** - Create and evaluate Agent skills
- **skills-index-updater/** - Regenerate the skill index
- **llms-dashboard/** - Generate LLM usage dashboards
- **humanize/** - Convert AI-written text to human-like writing

## Manual Setup (Alternative)

If you prefer to set up manually:

```bash
# Ensure .agent directory exists
mkdir -p ~/.agent

# Remove existing skills directory if needed
# rm -rf ~/.agent/skills

# Create symlink
ln -s ~/.claude/skills ~/.agent/skills
```
