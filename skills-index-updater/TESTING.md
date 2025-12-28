# Testing & Evaluation

Testing documentation for the Skill Index Updater.

## Testing Summary

| Model | Tested | Result |
|-------|--------|--------|
| Claude Haiku | Yes | Runs script correctly, follows workflow |
| Claude Sonnet | Yes | Reliable execution |
| Claude Opus | Yes | Comprehensive validation |

## Evaluation Scenarios

### Scenario 1: Standard Index Update

**Query:** "Update the skill index" or "Sync agents"

**Expected behaviors:**
- [ ] Runs `python3 .claude/skills/skills-index-updater/scripts/update_skill_index.py`
- [ ] Verifies output shows all expected skills
- [ ] Checks for any warnings during scan
- [ ] Reports success with skill count

**Failure indicators:**
- Running wrong script or command
- Not verifying output before comming back to the user
- Ignoring warnings about missing frontmatter

---

### Scenario 2: Dry Run Before Changes

**Query:** "Preview what the skill index update would do"

**Expected behaviors:**
- [ ] Uses `--dry-run` flag
- [ ] Shows what would be written without modifying files
- [ ] Allows user to verify before actual update

**Failure indicators:**
- Making changes without user confirmation
- Not mentioning dry-run option

---

### Scenario 3: Missing AGENTS.md Section

**Query:** "Update skill index" (but AGENTS.md lacks the index section)

**Expected behaviors:**
- [ ] Script reports error: "Available Skills Index not found"
- [ ] Suggests adding the section marker to AGENTS.md
- [ ] Does NOT crash or corrupt file

**Failure indicators:**
- Appending index to wrong location
- Silent failure

---

## Validation Commands

```bash
# Dry run to preview changes
python3 .claude/skills/skills-index-updater/scripts/update_skill_index.py --dry-run

# Count skills found
python3 .claude/skills/skills-index-updater/scripts/update_skill_index.py 2>&1 | grep "Found"

# Verify AGENTS.md was updated
git diff AGENTS.md
```

## Known Edge Cases

| Case | Expected Behavior |
|------|-------------------|
| Skill folder without SKILL.md | Warning printed, skill skipped |
| Invalid YAML in frontmatter | Warning printed, skill skipped |
| Missing name or description | Warning printed, skill skipped |
| Hidden folders (starting with .) | Automatically excluded |
| Very long description | Truncated in display, full in AGENTS.md |
