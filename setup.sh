#!/bin/bash

# Setup script for Agent Global Skills
# Creates a symlink from ~/.claude/skills to ~/.agent/skills

set -e

AGENT_SKILLS_DIR="$HOME/.agent/skills"
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"

echo "🔧 Setting up Agent Global Skills..."

# Ensure .claude directory exists
mkdir -p "$HOME/.claude"

# Check if .claude/skills already exists
if [ -e "$CLAUDE_SKILLS_DIR" ]; then
    if [ -L "$CLAUDE_SKILLS_DIR" ]; then
        echo "ℹ️  Symlink already exists at $CLAUDE_SKILLS_DIR"
        echo "   Points to: $(readlink "$CLAUDE_SKILLS_DIR")"
        exit 0
    else
        echo "⚠️  $CLAUDE_SKILLS_DIR already exists and is not a symlink."
        echo "   Please backup/remove it manually before running this script."
        exit 1
    fi
fi

# Create symlink
ln -s "$AGENT_SKILLS_DIR" "$CLAUDE_SKILLS_DIR"

echo "✅ Symlink created: $CLAUDE_SKILLS_DIR -> $AGENT_SKILLS_DIR"
echo ""
echo "Skills are now accessible from both locations:"
echo "  📁 $AGENT_SKILLS_DIR (source)"
echo "  🔗 $CLAUDE_SKILLS_DIR (symlink)"
