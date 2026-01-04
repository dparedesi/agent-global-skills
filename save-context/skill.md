---
name: save-context
description: Save session context for agent handoffs. Use when ending work, switching agents, or when user says "save context", "handoff", "wrap up", or "save session".
---

# Save Context

Generate a conversation summary for seamless agent handoffs.

## Scope

This skill captures ONLY what happened in the current chat session:
- User requests and goals from this conversation
- Actions taken by THIS agent in THIS session
- Decisions made during this session
- Pending work from this session

**DO NOT:**
- Run git commands (no `diff`, `log`, `commit`, `status`)
- Explore the filesystem with `ls`, `find`, etc.
- Gather information about the broader project/repository state
- Make any commits

The conversation history is already in your context. Extract from it directly.

## Workflow

1. **Analyze the conversation** — Review what was discussed, requested, and done
2. **Ask clarifying questions** (only if needed):
   - "What's the most important thing the next agent should know?"
   - "Any blockers or decisions pending your input?"
3. **Generate the context document**
4. **Save to `.context/`**
5. **Offer .gitignore protection** (if git repo exists)

## Template

Generate **only sections with content**. Omit empty sections entirely.

```markdown
# Session Handoff: [Brief Topic]
**Date:** YYYY-MM-DD HH:MM
**Status:** [ready to continue | blocked on X | needs decision]

## TL;DR
[2-3 sentences: what was requested, what happened, what's next]

---

## What Was Requested
[User's goal/task from this conversation - be specific]

## What Was Done
- [Specific action - include file paths if files were edited]
- [Another action]

## Pending / Blocked
- [What's left to do]
- **Blocked on:** [if applicable]

## Key Decisions
- **[Decision]:** [Why this choice was made]

## Files Touched This Session
[Only list files that THIS agent actually read/created/edited in THIS session]

| File | Action | What Changed |
|------|--------|--------------|
| `path/to/file` | Created/Modified/Read | Brief description |

## Known Issues Discovered
- [Issue found during this session]

## Continue From
[Direct instruction: where to pick up, what to do first]

---

**For next agent:** [One-line instruction on immediate next step]
```

## File Management

### Location & Naming

```
.context/
├── 2025-01-03-1430.md
└── 2025-01-02-0900.md
```

```bash
mkdir -p .context
FILENAME=".context/$(date +%Y-%m-%d-%H%M).md"
```

### Gitignore Protection

Context files should NEVER be pushed to remote repositories.

After saving the context file, check if this is a git repo and if `.context/` is protected:

```bash
if [ -d .git ]; then
    if [ -f .gitignore ] && grep -q "^\.context" .gitignore; then
        echo "Already protected"
    else
        echo "NOT protected - .context/ is not in .gitignore"
    fi
fi
```

If not protected, **ask the user:**

> ".context/ is not in your .gitignore. Add it to prevent accidentally pushing context files to your repo?"

Only modify `.gitignore` if the user confirms.

## Quality Checklist

Before saving:
- [ ] TL;DR alone gives clear picture of the session
- [ ] No empty sections or placeholders
- [ ] Only includes work from THIS session (not repo-wide state)
- [ ] "Continue From" is specific and actionable
- [ ] Can be understood without access to this chat

## Edge Cases

| Situation | Approach |
|-----------|----------|
| No meaningful work done | Don't generate a context file - tell the user |
| Only exploration/research | Document findings and recommendations |
| Multiple unrelated tasks | Create sections for each topic |
| Session was debugging | Emphasize findings, root cause, fix status |

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Run `git diff` or `git log` | Extract from conversation what YOU did |
| Paste chat history | Summarize key points |
| Include repo-wide file listings | Only files YOU touched this session |
| Vague "continue working" | Specific next action |
| Include "[TBD]" placeholders | Omit the section |
