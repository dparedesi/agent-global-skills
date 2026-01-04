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

- **cli-onboarding/** - First-time user experience for CLI packages (setup wizards, edge cases, validation)
- **commit-and-push/** - Automates git commit and push operations
- **elevate/** - Framework to transform code to production quality using 12 patterns
- **humanize/** - Convert AI-written text to human-like writing
- **inbox-assistant/** - AI-powered tool for managing and triaging Gmail inboxes
- **llms-dashboard/** - Generate dashboards to visualize LLM usage statistics
- **save-context/** - Save current session context for agent handoffs or pausing work
- **skill-builder/** - Create, evaluate, and scaffold new Agent skills
- **skills-index-updater/** - Regenerate the skill index for AGENTS.md
- **skills-local-setup/** - Set up symlinks for multi-agent compatibility (Claude, Gemini, etc.)
- **transcribe/** - Transcribe audio files with speaker diarization using VoxScriber

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
