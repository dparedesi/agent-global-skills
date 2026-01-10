---
name: synap-assistant
source: synap-cli
description: Manage a personal knowledge capture system. Use when the user wants to capture ideas, track todos, organize projects, review their synap, or mentions "synap", "brain dump", "capture this", "add to my list", "what's on my plate", "what should I focus on", or "daily review".
hash: 9c86041f8c7095822804f47de0b68715
---

# synap Assistant

A CLI for externalizing your working memory - capture ideas, projects, features, todos, and questions without the overhead of complex tools.

## Why?

Your brain is for having ideas, not holding them. But sticky notes get lost, notepads pile up unread, and tools like Asana are overkill for personal capture.

**synap** solves this by providing:
- **Zero-friction capture** - dump thoughts in seconds
- **Structured retrieval** - find anything with search and filters
- **AI-assisted triage** - agents help you organize, prioritize, and act

## Agent Mindset

When assisting users with their synap entries:

1. **Capture first, organize later** - Never block on classification during fast capture. Get the thought out, refine later.

2. **Proactive triage** - Regularly surface raw entries needing processing. Don't let the inbox grow stale.

3. **Connect the dots** - Link related entries, identify patterns, consolidate ideas into projects.

4. **Reduce cognitive load** - Present summaries and prioritized lists, not exhaustive dumps.

5. **Preserve context** - Include enough detail for future recall. A cryptic note is useless later.

6. **Respect simplicity** - Simple thoughts don't need tags, priorities, and parents. Don't over-engineer.

## User Preferences (Memory)

synap stores long-term user preferences at `~/.config/synap/user-preferences.md`.

- Read preferences at the start of a session when present.
- Append stable, reusable preferences with `synap preferences --append "## Section" "..."`.
- Avoid overwriting user-written content; prefer section-based appends.

## Operating Modes

Detect user intent and respond appropriately:

| Mode | Triggers | Behavior |
|------|----------|----------|
| **Capture** | "Add this...", "Remind me...", "I had an idea..." | Fast capture, minimal questions, default to idea type |
| **Review** | "What's on my plate?", "Daily review", "Show me..." | Stats + prioritized summary, grouped by type |
| **Triage** | "Process my synap", "Process my brain dump", "What needs attention?" | Surface raw entries, help classify and prioritize |
| **Focus** | "What should I work on?", "Priority items" | P1 todos + active projects, clear next actions |
| **Cleanup** | "Archive completed", "Clean up old stuff" | Bulk operations with preview and confirmation |

### Volume Modes (Quick vs Deep)

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Quick** | <10 entries returned | Direct answers, lightweight summaries, minimal batching |
| **Deep** | 10+ entries returned | Summarize first, propose batches, confirm before bulk actions |

## Quick Start

| Task | Command |
|------|---------|
| Capture idea | `synap add "your thought here"` |
| Add todo | `synap todo "task description"` |
| Add question | `synap question "what you're wondering"` |
| List active | `synap list` |
| See all | `synap list --all` |
| Search | `synap search "keyword"` |
| Show details | `synap show <id>` |
| Mark done | `synap done <id>` |
| Get stats | `synap stats` |
| Setup wizard | `synap setup` |
| Edit preferences | `synap preferences --edit` |

## Pre-flight Check

Before operations, verify the tool is ready:

```bash
synap --version   # Verify installed
synap stats       # Quick health check
```

If `synap: command not found`, the user needs to install: `npm install -g synap`

## Command Reference

### Capture Commands

#### `synap add <content>`
Quick capture of a thought.

```bash
synap add "What if we used a graph database?"
synap add "Need to review the API design" --type todo --priority 1
synap add "Meeting notes from standup" --type note --tags "meetings,weekly"
synap add --type project --title "Website Redesign" "Complete overhaul of the marketing site..."
```

**Options**:
- `--type <type>`: idea, project, feature, todo, question, reference, note (default: idea)
- `--title <title>`: Short title (auto-extracted from first line if not provided)
- `--priority <1|2|3>`: 1=high, 2=medium, 3=low
- `--tags <tags>`: Comma-separated tags
- `--parent <id>`: Parent entry ID
- `--json`: JSON output

#### `synap todo <content>`
Shorthand for adding a todo.

```bash
synap todo "Review PR #42"
# Equivalent to: synap add "Review PR #42" --type todo
```

#### `synap question <content>`
Shorthand for adding a question.

```bash
synap question "Should we migrate to TypeScript?"
# Equivalent to: synap add "..." --type question
```

### Query Commands

#### `synap list`
List entries with filtering.

```bash
synap list                              # Active + raw (default)
synap list --all                        # All except archived
synap list --type todo                  # Only todos
synap list --status raw                 # Needs triage
synap list --priority 1                 # High priority only
synap list --tags work,urgent           # Has ALL specified tags
synap list --since 7d                   # Created in last 7 days
synap list --json                       # JSON output for parsing
```

**Options**:
- `--type <type>`: Filter by entry type
- `--status <status>`: raw, active, someday, done, archived (default: raw,active)
- `--tags <tags>`: Comma-separated, AND logic
- `--priority <1|2|3>`: Filter by priority
- `--parent <id>`: Children of specific entry
- `--orphans`: Only entries without parent
- `--since <duration>`: e.g., 7d, 24h, 2w
- `--all`: All statuses except archived
- `--done`: Include done entries
- `--archived`: Show only archived
- `--limit <n>`: Max entries (default: 50)
- `--sort <field>`: created, updated, priority
- `--reverse`: Reverse sort order
- `--json`: JSON output

#### `synap show <id>`
Show full entry details.

```bash
synap show a1b2c3d4
synap show a1b2c3d4 --with-children
synap show a1b2c3d4 --with-related
synap show a1b2c3d4 --json
```

#### `synap search <query>`
Full-text search across content and titles.

```bash
synap search "database"
synap search "meeting" --type note --since 30d
synap search "API" --json
```

### Modify Commands

#### `synap edit <id>`
Edit entry content.

```bash
synap edit a1b2c3d4                          # Opens $EDITOR
synap edit a1b2c3d4 --content "New text"     # Non-interactive
synap edit a1b2c3d4 --append "Follow-up"     # Add to existing
synap edit a1b2c3d4 --title "New title"
```

#### `synap set <id>`
Update entry metadata.

```bash
synap set a1b2c3d4 --type project
synap set a1b2c3d4 --status active
synap set a1b2c3d4 --priority 1
synap set a1b2c3d4 --tags "work,Q1"
synap set a1b2c3d4 --add-tags "important"
synap set a1b2c3d4 --remove-tags "draft"
synap set a1b2c3d4 --clear-priority
synap set a1b2c3d4 --parent b2c3d4e5
```

#### `synap link <id1> <id2>`
Create relationships between entries.

```bash
synap link a1b2c3d4 b2c3d4e5                # Add to related
synap link a1b2c3d4 b2c3d4e5 --as-parent    # Set hierarchy
synap link a1b2c3d4 b2c3d4e5 --unlink       # Remove relationship
```

### Bulk Commands

#### `synap done <ids...>`
Mark entries as done.

```bash
synap done a1b2c3d4
synap done a1b2c3d4 b2c3d4e5 c3d4e5f6       # Multiple
synap done --type todo --tags "sprint-1"     # By filter
synap done --dry-run --type todo             # Preview first
```

#### `synap archive <ids...>`
Archive entries (hides from default view).

```bash
synap archive a1b2c3d4
synap archive --status done --since 30d      # Old completed items
synap archive --dry-run --status done        # Preview
```

#### `synap delete <ids...>`
Delete entries (logged for undo).

```bash
synap delete a1b2c3d4
synap delete a1b2c3d4 b2c3d4e5 --confirm
synap delete --status archived --since 90d   # Permanent cleanup
synap delete --dry-run --type reference      # Preview
```

**Safety**:
- All deletions logged to enable restore
- >10 entries requires `--confirm` or `--force`
- Entries with children require `--force`

#### `synap restore`
Restore deleted entries.

```bash
synap restore --last 1                       # Most recent
synap restore --last 5                       # Last 5
synap restore --ids a1b2c3d4,b2c3d4e5        # Specific IDs
synap restore --list                         # Show deletion log
```

### Maintenance Commands

#### `synap stats`
Overview statistics.

```bash
synap stats
synap stats --json
```

#### `synap export`
Export entries.

```bash
synap export                                 # All to stdout
synap export --file backup.json              # To file
synap export --type todo --status active     # Filtered
```

#### `synap import <file>`
Import entries.

```bash
synap import backup.json
synap import backup.json --dry-run
synap import backup.json --merge             # Update existing + add new
synap import backup.json --skip-existing     # Only add new
```

## Workflow Patterns

### Daily Review

Run this each morning to get oriented:

1. **Health check**: `synap stats`
2. **Triage raw entries**: `synap list --status raw`
3. **Focus list**: `synap list --priority 1 --type todo`
4. **Help user decide** what to work on first

### Weekly Review

Run this weekly to maintain hygiene:

1. **Celebrate**: `synap list --done --since 7d` - show what was accomplished
2. **Check stalled**: `synap list --status active --sort updated` - find items not touched
3. **Review projects**: `synap list --type project` - are they progressing?
4. **Clean up**: `synap archive --status done --since 7d` - archive completed items

### Triage Workflow

When user has many raw entries:

1. **Fetch**: `synap list --status raw --json`
2. **For each entry**, determine:
   - Type (idea, todo, project, question, reference, note)
   - Priority (1, 2, 3, or none)
   - Tags (infer from content)
   - Parent (if belongs to existing project/feature)
3. **Update**: `synap set <id> --type todo --priority 1 --tags "work"`
4. **If entry is actually multiple items**, split and re-capture
5. **Mark refined**: `synap set <id> --status active`

### Capture Mode

When user is dumping thoughts rapidly:

1. Just capture with `synap add "..."` - don't interrupt for classification
2. Use default type (idea) and status (raw)
3. After the capture session, offer to triage

## Classification Rules

### Type Detection Heuristics

| Indicator | Likely Type |
|-----------|-------------|
| Starts with action verb ("Build", "Write", "Fix", "Review") | `todo` |
| Contains "?" or seeking information | `question` |
| Multi-step initiative, long-term scope | `project` |
| Specific capability/enhancement within a project | `feature` |
| Link, quote, or factual information | `reference` |
| Observation with no clear action | `note` |
| Speculative, "what if", creative | `idea` |

### Priority Assignment

| Priority | Criteria |
|----------|----------|
| P1 (high) | Blocking other work, deadline within 48h, explicitly urgent |
| P2 (medium) | Important but not urgent, this-week scope |
| P3 (low) | Nice-to-have, someday-maybe, learning/exploration |
| None | Truly unprioritized, needs triage |

## Safety Rules

**Non-negotiable constraints**:

1. **Never auto-delete** - Always show what will be deleted and confirm
2. **Preserve context** - Don't summarize away important details during capture
3. **Log before delete** - All deletions are recoverable via `synap restore`
4. **Confirm bulk operations** - Operations affecting >10 entries require confirmation
5. **Don't over-organize** - Simple thoughts don't need tags, priorities, and parents

## Proactive Recommendation Patterns

- If raw entries are piling up, suggest `synap triage`.
- If P1 todos exist, suggest `synap focus`.
- If many stale active items exist, suggest a weekly review.
- If preferences specify cadence, follow it by default.

## Batch Processing Protocols

- Filters are for discovery; use IDs for execution.
- Keep batches small (10-25 items) and confirm between batches.
- Use `--dry-run` whenever available before bulk changes.

## Two-Step Pattern for Bulk Operations

Critical for preventing accidental mass changes:

1. **Preview**: `synap delete --status archived --since 90d --dry-run`
2. **Confirm**: Show user what will be affected, get explicit approval
3. **Execute**: `synap delete --ids "<specific-ids>" --confirm`

**Principle**: Filters are for DISCOVERY, IDs are for EXECUTION.

## Common Request Patterns

| User Says | Interpretation | Action |
|-----------|----------------|--------|
| "Add this to my synap" | Fast capture | `synap add "<content>"` |
| "I need to remember to..." | Todo item | `synap todo "<content>"` |
| "What's on my plate?" | Need overview | `synap stats` + `synap list --priority 1` |
| "What should I focus on?" | Need priorities | `synap list --priority 1 --type todo` |
| "Process my synap" | Triage needed | Run triage workflow on raw entries |
| "This is done" / "I finished X" | Mark complete | `synap done <id>` |
| "Archive old stuff" | Cleanup | `synap archive --status done --since 30d` |
| "What did I do this week?" | Review completions | `synap list --done --since 7d` |
| "Find anything about X" | Search | `synap search "X"` |
| "Link these together" | Create relationship | `synap link <id1> <id2>` |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `synap: command not found` | Run `npm install -g synap` |
| Empty synap | Start with `synap add "My first thought"` |
| Too many raw entries | Run triage workflow |
| Can't find entry | Use `synap search "<keyword>"` |
| Accidentally deleted | Use `synap restore --last 1` |
| Wrong type/status | Use `synap set <id> --type <type> --status <status>` |

## Testing / Evaluation Scenarios

| Scenario | Expected Behavior | Failure Indicator |
|----------|-------------------|-------------------|
| User says "capture this" | Immediate `synap add`, no questions | Asking for type/priority during fast capture |
| User says "what's on my plate" | Stats + prioritized summary | Listing all 50 entries individually |
| User says "clean up" | Preview + confirmation | Auto-archiving without preview |
| Large deletion (>10 items) | Show count, ask confirmation | Proceeding without confirmation |
| User mentions deadline | Suggest P1 priority | Not detecting urgency |
| User's idea relates to existing project | Suggest linking | Not checking for related entries |

## JSON Output Schemas

### Entry Object

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "content": "The full text of the entry",
  "title": "Short title (optional)",
  "type": "idea|project|feature|todo|question|reference|note",
  "status": "raw|active|someday|done|archived",
  "priority": 1|2|3|null,
  "tags": ["tag1", "tag2"],
  "parent": "parent-id|null",
  "related": ["id1", "id2"],
  "createdAt": "2026-01-05T08:30:00.000Z",
  "updatedAt": "2026-01-05T08:30:00.000Z",
  "source": "cli|agent|import"
}
```

### List Response

```json
{
  "success": true,
  "entries": [...],
  "total": 47,
  "returned": 12,
  "query": {
    "status": ["raw", "active"],
    "limit": 50
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": "Entry not found: a1b2c3d4",
  "code": "ENTRY_NOT_FOUND"
}
```

## Remember

- The goal is to **externalize working memory**, not build a perfect system
- Capture is king - never block a capture
- Structure serves retrieval, not organizational perfection
- The best system is one that gets used
