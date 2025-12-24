#!/bin/bash

# Setup Local Skills - Create symlinks for AI tools in the current repository
# Usage: ./setup-local-skills.sh [gemini|claude|cursor|all]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in a git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi

REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

# Function to add entry to .gitignore if not present
add_to_gitignore() {
    local entry="$1"
    if [ ! -f .gitignore ]; then
        echo "# AI tool symlinks" > .gitignore
    fi
    if ! grep -q "^${entry}$" .gitignore 2>/dev/null; then
        echo "$entry" >> .gitignore
        echo -e "${GREEN}✓${NC} Added '$entry' to .gitignore"
    else
        echo -e "${YELLOW}ℹ${NC} '$entry' already in .gitignore"
    fi
}

# Function to create symlink safely
create_symlink() {
    local source="$1"
    local target="$2"
    local gitignore_entry="$3"
    
    if [ -L "$target" ]; then
        echo -e "${YELLOW}ℹ${NC} Symlink already exists: $target -> $(readlink "$target")"
    elif [ -e "$target" ]; then
        echo -e "${RED}⚠${NC} $target exists but is not a symlink. Skipping."
        echo "   To replace, run: rm -rf $target && ln -s $source $target"
        return 1
    else
        ln -s "$source" "$target"
        echo -e "${GREEN}✓${NC} Created: $target -> $source"
    fi
    
    add_to_gitignore "$gitignore_entry"
}

# Setup Gemini
setup_gemini() {
    echo ""
    echo "🔷 Setting up Gemini..."
    
    if [ ! -f AGENTS.md ]; then
        echo -e "${RED}Error: AGENTS.md not found in repo root${NC}"
        return 1
    fi
    
    create_symlink "AGENTS.md" "GEMINI.md" "GEMINI.md"
}

# Setup Claude
setup_claude() {
    echo ""
    echo "🟣 Setting up Claude..."
    
    mkdir -p .claude
    
    # Skills symlink
    if [ -d .agent/skills ]; then
        create_symlink "../.agent/skills" ".claude/skills" ".claude/"
    elif [ -d "$HOME/.agent/skills" ]; then
        echo -e "${YELLOW}ℹ${NC} No local .agent/skills, skipping (global skills available via ~/.agent/skills)"
    else
        echo -e "${YELLOW}ℹ${NC} No .agent/skills directory found, skipping skills symlink"
    fi
    
    # Settings symlink
    if [ -f .agent/settings.json ]; then
        create_symlink "../.agent/settings.json" ".claude/settings.json" ".claude/"
    else
        echo -e "${YELLOW}ℹ${NC} No .agent/settings.json found, skipping settings symlink"
    fi
    
    # Ensure .claude/ is in gitignore even if no symlinks created
    add_to_gitignore ".claude/"
}

# Setup Cursor
setup_cursor() {
    echo ""
    echo "🔵 Setting up Cursor..."
    
    if [ ! -f AGENTS.md ]; then
        echo -e "${RED}Error: AGENTS.md not found in repo root${NC}"
        return 1
    fi
    
    create_symlink "AGENTS.md" ".cursorrules" ".cursorrules"
}

# Show usage
show_usage() {
    echo "Usage: $0 [gemini|claude|cursor|all]"
    echo ""
    echo "Options:"
    echo "  gemini  - Create GEMINI.md symlink to AGENTS.md"
    echo "  claude  - Create .claude/skills -> .agent/skills symlink"
    echo "  cursor  - Create .cursorrules symlink to AGENTS.md"
    echo "  all     - Setup all tools"
    echo ""
    echo "Examples:"
    echo "  $0 gemini      # Setup Gemini only"
    echo "  $0 all         # Setup all tools"
}

# Main
case "${1:-}" in
    gemini)
        setup_gemini
        ;;
    claude)
        setup_claude
        ;;
    cursor)
        setup_cursor
        ;;
    all)
        setup_gemini
        setup_claude
        setup_cursor
        ;;
    -h|--help|"")
        show_usage
        exit 0
        ;;
    *)
        echo -e "${RED}Unknown option: $1${NC}"
        show_usage
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Verify with:"
echo "  ls -la GEMINI.md .cursorrules .claude/ 2>/dev/null"
echo "  git status"
