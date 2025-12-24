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
        echo ""
        echo "📁 Current contents:"
        ls -la "$CLAUDE_SKILLS_DIR" 2>/dev/null | head -20
        echo ""
        
        # Count items (excluding . and ..)
        ITEM_COUNT=$(find "$CLAUDE_SKILLS_DIR" -mindepth 1 | wc -l | tr -d ' ')
        if [ "$ITEM_COUNT" -gt 0 ]; then
            echo "⚠️  This folder contains $ITEM_COUNT item(s) that will be DELETED."
        else
            echo "ℹ️  This folder is empty."
        fi
        echo ""
        
        read -p "Do you want to remove $CLAUDE_SKILLS_DIR and create the symlink? [y/N] " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "🗑️  Removing $CLAUDE_SKILLS_DIR..."
            rm -rf "$CLAUDE_SKILLS_DIR"
        else
            echo "❌ Setup cancelled. No changes made."
            exit 1
        fi
    fi
fi

# Create symlink
ln -s "$AGENT_SKILLS_DIR" "$CLAUDE_SKILLS_DIR"

echo "✅ Symlink created: $CLAUDE_SKILLS_DIR -> $AGENT_SKILLS_DIR"
echo ""
echo "Skills are now accessible from both locations:"
echo "  📁 $AGENT_SKILLS_DIR (source)"
echo "  🔗 $CLAUDE_SKILLS_DIR (symlink)"
