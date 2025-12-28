#!/bin/bash

# Setup script for Agent Global Skills
# Creates a symlink from ~/.agent/skills to ~/.claude/skills
# (Skills live in ~/.claude/skills, symlink provides backward compatibility)

set -e

CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
AGENT_SKILLS_DIR="$HOME/.agent/skills"

echo "🔧 Setting up Agent Global Skills..."

# Ensure .agent directory exists
mkdir -p "$HOME/.agent"

# Check if .agent/skills already exists
if [ -e "$AGENT_SKILLS_DIR" ]; then
    if [ -L "$AGENT_SKILLS_DIR" ]; then
        echo "ℹ️  Symlink already exists at $AGENT_SKILLS_DIR"
        echo "   Points to: $(readlink "$AGENT_SKILLS_DIR")"
        exit 0
    else
        echo "⚠️  $AGENT_SKILLS_DIR already exists and is not a symlink."
        echo ""
        echo "📁 Current contents:"
        ls -la "$AGENT_SKILLS_DIR" 2>/dev/null | head -20
        echo ""

        # Count items (excluding . and ..)
        ITEM_COUNT=$(find "$AGENT_SKILLS_DIR" -mindepth 1 | wc -l | tr -d ' ')
        if [ "$ITEM_COUNT" -gt 0 ]; then
            echo "⚠️  This folder contains $ITEM_COUNT item(s) that will be DELETED."
        else
            echo "ℹ️  This folder is empty."
        fi
        echo ""

        read -p "Do you want to remove $AGENT_SKILLS_DIR and create the symlink? [y/N] " -n 1 -r
        echo ""

        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "🗑️  Removing $AGENT_SKILLS_DIR..."
            rm -rf "$AGENT_SKILLS_DIR"
        else
            echo "❌ Setup cancelled. No changes made."
            exit 1
        fi
    fi
fi

# Create symlink
ln -s "$CLAUDE_SKILLS_DIR" "$AGENT_SKILLS_DIR"

echo "✅ Symlink created: $AGENT_SKILLS_DIR -> $CLAUDE_SKILLS_DIR"
echo ""
echo "Skills are now accessible from both locations:"
echo "  📁 $CLAUDE_SKILLS_DIR (source)"
echo "  🔗 $AGENT_SKILLS_DIR (symlink)"
