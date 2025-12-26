#!/usr/bin/env python3
"""
Skill Index Updater - Regenerate the Available Skill Index in AGENTS.md

This script scans both local and global skill directories, extracts frontmatter
from SKILL.md files, and updates the index section in AGENTS.md.

Architecture Note:
    - Local skills: `.agent/skills/` in the current repo (project-specific)
    - Global skills: `~/.agent/skills/` (available across all repos)
    - Both are listed in AGENTS.md for VS Code/Kiro compatibility
    - Skills are grouped by scope (Global first, then Local)

Usage:
    python update_skill_index.py
    python update_skill_index.py --dry-run

Requirements:
    - Python 3.8+
    - PyYAML (pip install pyyaml)
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Try PyYAML, fall back to regex parsing if unavailable
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


def parse_yaml_fallback(text: str) -> Optional[Dict]:
    """Simple regex-based YAML parser for basic key: value frontmatter."""
    result = {}
    for line in text.strip().split("\n"):
        match = re.match(r'^(\w+):\s*(.+)$', line.strip())
        if match:
            result[match.group(1)] = match.group(2).strip()
    return result if result else None

# Paths
GLOBAL_SKILLS_DIR = Path.home() / ".agent" / "skills"

# Local paths - determined at runtime based on where script is invoked
# When running from a repo, we find the repo's .agent/skills/ directory
def find_repo_root() -> Optional[Path]:
    """Find the repository root by looking for .git directory."""
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".git").exists():
            return parent
    return None

REPO_ROOT = find_repo_root()
LOCAL_SKILLS_DIR = REPO_ROOT / ".agent" / "skills" if REPO_ROOT else None
AGENTS_MD = REPO_ROOT / "AGENTS.md" if REPO_ROOT else None

# Path prefixes for generated index
LOCAL_SKILLS_PATH_PREFIX = ".agent/skills"
GLOBAL_SKILLS_PATH_PREFIX = "~/.agent/skills"


# Markers for the index section
INDEX_START = "## Available Skills Index"
INDEX_END = "---"


def parse_frontmatter(skill_path: Path) -> Optional[Dict]:
    """
    Parse YAML frontmatter from a SKILL.md file.

    Args:
        skill_path: Path to SKILL.md file

    Returns:
        Dict with 'name' and 'description', or None if parsing fails
    """
    try:
        content = skill_path.read_text(encoding="utf-8")
    except (IOError, OSError) as e:
        print(f"  Warning: Cannot read {skill_path}: {e}", file=sys.stderr)
        return None

    # Match frontmatter between --- markers
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        print(f"  Warning: No frontmatter found in {skill_path}", file=sys.stderr)
        return None

    # Parse YAML (with fallback if PyYAML unavailable)
    if YAML_AVAILABLE:
        try:
            frontmatter = yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            print(f"  Warning: Invalid YAML in {skill_path}: {e}", file=sys.stderr)
            return None
    else:
        frontmatter = parse_yaml_fallback(match.group(1))
        if not frontmatter:
            print(f"  Warning: Could not parse frontmatter in {skill_path}", file=sys.stderr)
            return None

    if not frontmatter or "name" not in frontmatter or "description" not in frontmatter:
        print(f"  Warning: Missing name/description in {skill_path}", file=sys.stderr)
        return None

    return {
        "name": frontmatter["name"],
        "description": frontmatter["description"],
        "folder": skill_path.parent.name,
    }


def scan_skills_dir(skills_dir: Path, scope: str, path_prefix: str) -> List[Dict]:
    """
    Scan a skill directory and extract frontmatter.

    Args:
        skills_dir: Path to the skills directory to scan
        scope: "global" or "local" - used for labeling
        path_prefix: Path prefix for display (e.g., ".agent/skills" or "~/.agent/skills")

    Returns:
        List of skill dicts sorted by name
    """
    skills = []

    if not skills_dir or not skills_dir.exists():
        return skills

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith("."):
            continue

        # A directory is only a skill if it contains SKILL.md
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        skill_data = parse_frontmatter(skill_file)
        if skill_data:
            skill_data["scope"] = scope
            skill_data["path_prefix"] = path_prefix
            skills.append(skill_data)

    return sorted(skills, key=lambda s: s["name"])


def generate_index(global_skills: List[Dict], local_skills: List[Dict], include_global: bool = False) -> str:
    """
    Generate the markdown index section with skills grouped by scope.

    Args:
        global_skills: List of global skill dicts
        local_skills: List of local skill dicts
        include_global: Whether global skills were requested (affects output format)

    Returns:
        Formatted markdown string
    """
    lines = [
        INDEX_START,
        "_This index is for IDEs that don't natively support skills (e.g., Gemini CLI, Kiro). Skip if your IDE reads SKILL.md directly._",
        "",
    ]

    # Global skills section (only if present)
    if global_skills:
        lines.append("### Global Skills")
        lines.append("*Available across all repositories*")
        lines.append("")
        for skill in global_skills:
            lines.append(f"- **Name:** `{skill['name']}`")
            lines.append(f"  - **Trigger:** {skill['description']}")
            lines.append(f"  - **Path:** `{skill['path_prefix']}/{skill['folder']}/SKILL.md`")
            lines.append("")

    # Local skills section
    if local_skills:
        # Only show section header if we also have global skills
        if global_skills:
            lines.append("### Local Skills")
            lines.append("*Specific to this repository*")
            lines.append("")
        for skill in local_skills:
            lines.append(f"- **Name:** `{skill['name']}`")
            lines.append(f"  - **Trigger:** {skill['description']}")
            lines.append(f"  - **Path:** `{skill['path_prefix']}/{skill['folder']}/SKILL.md`")
            lines.append("")

    return "\n".join(lines)


def update_agents_md(new_index: str, dry_run: bool = False) -> bool:
    """
    Update the index section in AGENTS.md.

    Args:
        new_index: New index content to insert
        dry_run: If True, print changes without writing

    Returns:
        True if successful, False otherwise
    """
    if not AGENTS_MD.exists():
        print(f"Error: {AGENTS_MD} not found", file=sys.stderr)
        return False

    content = AGENTS_MD.read_text(encoding="utf-8")

    # Find the index section
    start_match = re.search(rf"^{re.escape(INDEX_START)}.*$", content, re.MULTILINE)
    if not start_match:
        print(f"Error: '{INDEX_START}' header not found in {AGENTS_MD}", file=sys.stderr)
        print(f"  Tip: Add this line to your file: {INDEX_START}", file=sys.stderr)
        return False

    # Find the next --- after the index (or end of file)
    end_match = re.search(rf"^{re.escape(INDEX_END)}\s*$", content[start_match.start():], re.MULTILINE)
    if end_match:
        end_pos = start_match.start() + end_match.start()
        new_content = content[:start_match.start()] + new_index + "\n" + content[end_pos:]
    else:
        # No closing marker found - append to end of index section
        print(f"  Note: No closing '---' marker found. Appending index to end of section.")
        new_content = content[:start_match.start()] + new_index + "\n---\n"

    if dry_run:
        print("\n=== DRY RUN: Would write ===")
        print(new_index)
        print("=== END ===\n")
        return True

    AGENTS_MD.write_text(new_content, encoding="utf-8")
    return True


AGENTS_MD_TEMPLATE = """# Agents and Skills

This file documents the agents and skills available in this repository.

## Available Skills Index

---
"""


def init_agents_md(dry_run: bool = False) -> bool:
    """Create AGENTS.md with default template."""
    if dry_run:
        print(f"\n=== DRY RUN: Would create {AGENTS_MD} ===")
        print(AGENTS_MD_TEMPLATE)
        print("=== END ===\n")
        return True
    
    AGENTS_MD.write_text(AGENTS_MD_TEMPLATE, encoding="utf-8")
    print(f"Created: {AGENTS_MD}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Update the skill index in AGENTS.md (scans both global and local skills)"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would be written without making changes"
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Create AGENTS.md if it doesn't exist (auto-prompted if missing)"
    )
    args = parser.parse_args()

    # Check we're in a repo
    if not REPO_ROOT:
        print("Error: Not in a git repository. Run from within a repo.", file=sys.stderr)
        sys.exit(1)

    # Auto-initialize AGENTS.md if missing
    if not AGENTS_MD.exists():
        if args.init:
            if not init_agents_md(args.dry_run):
                sys.exit(1)
        else:
            print(f"AGENTS.md not found at: {AGENTS_MD}")
            response = input("Create it now? [Y/n]: ").strip().lower()
            if response in ("", "y", "yes"):
                if not init_agents_md(args.dry_run):
                    sys.exit(1)
            else:
                print("Aborted. Run with --init to create automatically.")
                sys.exit(1)

    # Determine whether to include global skills
    # ALWAYS prompt the user - NO FLAGS can bypass this (prevents AI agents from running unattended)
    print("\n" + "="*60)
    response = input("Include global skills from ~/.agent/skills/? [y/N]: ").strip().lower()
    print("="*60 + "\n")
    include_global = response in ("y", "yes")

    # Scan global skills (only if user confirmed)
    global_skills = []
    if include_global:
        print(f"Scanning global skills in: {GLOBAL_SKILLS_DIR}")
        global_skills = scan_skills_dir(GLOBAL_SKILLS_DIR, "global", GLOBAL_SKILLS_PATH_PREFIX)
        print(f"  Found {len(global_skills)} global skills")
    else:
        print("Skipping global skills (user declined)")

    # Scan local skills
    print(f"Scanning local skills in: {LOCAL_SKILLS_DIR}")
    local_skills = scan_skills_dir(LOCAL_SKILLS_DIR, "local", LOCAL_SKILLS_PATH_PREFIX)
    print(f"  Found {len(local_skills)} local skills")

    total_skills = len(global_skills) + len(local_skills)
    if total_skills == 0:
        print("No skills found!", file=sys.stderr)
        sys.exit(1)

    print(f"\nTotal: {total_skills} skills")
    if global_skills:
        print("  Global:")
        for s in global_skills:
            print(f"    - {s['name']} ({s['folder']})")
    if local_skills:
        print("  Local:")
        for s in local_skills:
            print(f"    - {s['name']} ({s['folder']})")

    new_index = generate_index(global_skills, local_skills, include_global=include_global)

    if update_agents_md(new_index, dry_run=args.dry_run):
        if args.dry_run:
            print("\nDry run complete. No changes made.")
        else:
            print(f"\nUpdated: {AGENTS_MD}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
