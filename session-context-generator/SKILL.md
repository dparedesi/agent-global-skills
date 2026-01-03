---
name: session-context-generator
description: Generate comprehensive session context restoration files for agent handoffs. Use when ending a session, creating agent handoff documentation, saving work context for future agents, or when the user mentions "save context", "handoff to another agent", "restore context", or "session summary".
---

# Session Context Generator

Generate comprehensive context restoration documents that enable seamless agent handoffs.

**Why?** When switching between agents or ending a session, critical context about the project, decisions made, implementations completed, and pending work can be lost. This skill creates a structured handoff document that allows any future agent to continue exactly where you left off.

## Quick Start

1. Gather session information → 2. Generate context document → 3. Validate document → 4. Save to restore-context/ folder → 5. Ensure restore-context/ is in .gitignore → Done

## Prerequisites

Before generating a session context file:
- [ ] Have completed meaningful work in the current session
- [ ] Know what was implemented vs. what's pending
- [ ] Have access to the project repository
- [ ] Understand the project's current state

## Generation Process

### 1. Gather Session Information

Collect the following information from the user or session:

**Project Details:**
- Project name and description
- Repository location and structure
- Current state (connected to git? deployment status?)

**Session Work:**
- What was accomplished in this session
- What files were created/modified
- What issues were identified
- What remains to be done

**Technical Context:**
- User's configuration/setup
- Key architectural decisions
- Critical files and their purposes
- Important behavioral patterns observed

**Next Steps:**
- Immediate testing required
- Short-term priorities
- Long-term roadmap items
- Questions for next agent to ask

### 2. Generate the Context Document

Use the template below, filling in all sections with specific details:

> [!IMPORTANT]
> The context document should be **comprehensive and actionable**. A future agent should be able to pick up work immediately without asking basic questions.

**File naming convention:**
```
restore-context/session-context-YYMMDDHHMMSS.md
```

Where:
- `YY` = Last 2 digits of year (e.g., 25 for 2025)
- `MM` = Month (01-12)
- `DD` = Day (01-31)
- `HH` = Hour in 24-hour format (00-23)
- `MM` = Minute (00-59)
- `SS` = Second (00-59)

Example: `session-context-251231130602.md` = 2025-12-31 at 13:06:02

### 3. Validate the Document

Before finalizing, check:

- [ ] All sections are filled with specific details (no placeholder text)
- [ ] File paths are absolute and accurate
- [ ] Commands include full syntax
- [ ] Technical details are precise (no vague descriptions)
- [ ] Next steps are actionable
- [ ] "What NOT to do" section prevents common mistakes
- [ ] Questions for next agent are relevant

### 4. Save the File

Create the file in the `restore-context/` directory:

```bash
# Ensure directory exists
mkdir -p restore-context

# File will be created at:
# restore-context/session-context-YYMMDDHHMMSS.md
```

> [!TIP]
> Include a note in the document about what log files or other artifacts were generated during the session that the next agent might want to review.

### 5. Ensure restore-context is in .gitignore

The `restore-context/` folder should NOT be committed to version control. It contains session-specific context that may include sensitive work-in-progress details.

**Check and update .gitignore:**

```bash
# Check if .gitignore exists and if restore-context is already ignored
if [ -f .gitignore ]; then
    if ! grep -q "^restore-context" .gitignore; then
        echo "restore-context/" >> .gitignore
        echo "Added restore-context/ to .gitignore"
    else
        echo "restore-context/ already in .gitignore"
    fi
else
    echo "restore-context/" > .gitignore
    echo "Created .gitignore with restore-context/"
fi
```

> [!WARNING]
> Always verify `restore-context/` is in `.gitignore` before completing the handoff. Session context files should remain local and not be pushed to remote repositories.

**Validation:**
- [ ] `.gitignore` file exists in project root
- [ ] `restore-context/` entry is present in `.gitignore`
- [ ] Running `git status` does not show `restore-context/` as untracked (if git repo)

## Document Template

```markdown
# Context Restoration - [Project Name] Session
**Date:** YYYY-MM-DD
**Session ID:** YYMMDDHHMMSS
**Status:** Ready for continuation

---

## Project Overview

[2-3 paragraph description of what the project does, its key value proposition, and current deployment status]

**Repository State:**
- [Git connection status]
- [Branch information]
- [Any pending commits/changes]

**User's Configuration:**
```json
{
  "key1": "value1",
  "key2": "value2"
}
```

[Explanation of the user's specific setup/configuration]

---

## What Happened in This Session

### 1. [Major Accomplishment 1]
[Detailed description of what was done]

**Files Modified:**
- `path/to/file1.js` - [What changed]
- `path/to/file2.js` - [What changed]

### 2. [Major Accomplishment 2]
[Detailed description]

**Files Created:**
- `path/to/newfile.js` - [Purpose]

### 3. [Analysis/Investigation Completed]
[What was learned, what logs were analyzed, what patterns were found]

---

## Current Repository Structure

```
project-root/
├── src/
│   ├── module1.js  # [Purpose] (MODIFIED/NEW/UNCHANGED)
│   └── module2.js  # [Purpose]
├── config/
│   └── settings.json  # [Purpose] (MODIFIED)
└── README.md
```

[Brief explanation of key directories and recent changes]

---

## Key Technical Details

### [Important Pattern 1]
[Explanation of how something works, with code examples if relevant]

### [Important Pattern 2]
[Technical details that next agent needs to understand]

### [Critical Constraints]
[Any important limitations, requirements, or gotchas]

---

## Testing Notes

### How to Test
```bash
# Command 1
command --with-args

# Command 2
another-command
```

### What to Verify
- [ ] [Test 1]
- [ ] [Test 2]
- [ ] [Test 3]

---

## Known Issues & Limitations

### Issue 1: [Name]
**Problem:** [Description]
**Workaround:** [How to handle it]
**Proposal:** [Potential fix]

### Issue 2: [Name]
[Same structure]

---

## Next Steps & Recommendations

### Immediate Testing
1. [What to test first]
2. [What to verify]

### Short-term (Next Session)
1. [Priority 1]
2. [Priority 2]

### Long-term Roadmap
1. [Future improvement 1]
2. [Future improvement 2]

---

## Important Context for Next Agent

### User's Preferences
1. [Preference 1]
2. [Preference 2]

### What NOT to Do
- [Anti-pattern 1 - explanation]
- [Anti-pattern 2 - explanation]

### What TO Do
- [Best practice 1]
- [Best practice 2]

### Critical Files to Understand Before Changes
1. **path/to/critical/file.js** - [Why it's critical]
2. **path/to/another/file.js** - [Why it's critical]

---

## Questions for Next Agent to Ask User

If continuing work, consider asking:
1. "[Question about current state]"
2. "[Question about priorities]"
3. "[Question about approach]"

---

## Session Completion Status

✅ **Completed:**
- [Item 1]
- [Item 2]

📋 **Pending:**
- [Item 1]
- [Item 2]

🎯 **Ready for:**
- [What next agent can immediately do]

---

## Reference Commands

### Development
```bash
npm install    # Install dependencies
npm start      # Start server
npm test       # Run tests
```

### Debugging
```bash
# [Description of what this does]
command --debug

# [Description]
another-command --verbose
```

---

## Final Notes

[Any additional context, gotchas, or important observations that don't fit elsewhere]

**Next agent:** [Direct message to the future agent about where to start]

---

**End of Context Document**
**Agent Handoff Ready** ✅
```

## Examples

### Example 1: After Bug Fix Session

**Context:** Session spent debugging and fixing a critical bug

**Generated File:** `restore-context/session-context-251231103022.md`

**Key Sections:**
- Project Overview: 2 paragraphs on the app + bug impact
- What Happened: Detailed bug investigation, root cause, fix implemented
- Files Modified: 3 files with specific changes explained
- Testing Notes: How to verify the fix works
- Next Steps: Deploy to production, monitor for regression

### Example 2: After Feature Implementation

**Context:** Session implementing a new authentication system

**Generated File:** `restore-context/session-context-251231140000.md`

**Key Sections:**
- Project Overview: Description + new auth architecture
- What Happened: Step-by-step implementation details
- Repository Structure: New auth/ directory explained
- Key Technical Details: JWT flow, session management
- Testing Notes: Auth test scenarios
- Next Steps: Integration testing, security review

### Example 3: After Analysis Session

**Context:** Session analyzing logs and creating improvement proposals

**Generated File:** `restore-context/session-context-251231160000.md`

**Key Sections:**
- Project Overview: System description + performance concerns
- What Happened: Log analysis, pattern identification
- Key Technical Details: Rate limiting behavior, caching patterns
- Known Issues: 5 issues documented with evidence
- Next Steps: Proposals document created, waiting for prioritization

## Quality Guidelines

> [!WARNING]
> **Never use placeholder text like "[TBD]" or "[Fill this in]"**. Every section must have real, specific information. If you don't have the information, gather it before generating the document.

**Document Quality Checklist:**
- [ ] **Specific**: No vague descriptions like "some files were changed"
- [ ] **Actionable**: Next agent knows exactly what to do
- [ ] **Complete**: All sections filled with meaningful content
- [ ] **Accurate**: File paths, commands, and technical details are correct
- [ ] **Contextual**: Explains WHY things were done, not just WHAT
- [ ] **Forward-looking**: Clear guidance on next steps
- [ ] **Self-contained**: Can be understood without reading chat history

**File Naming:**
- Use exact timestamp format: YYMMDDHHMMSS (no dashes between date and time)
- Example: `251231130602` NOT `251231-130602`
- Place in `restore-context/` directory
- Use `.md` extension

**Content Balance:**
- Comprehensive but not overwhelming
- Technical details without jargon overload
- Examples where they clarify, not for padding
- Tables for structured information
- Code blocks for commands and configurations

## Anti-Patterns to Avoid

**❌ Don't:**
- Create generic context documents with placeholder text
- Skip sections because "the next agent will figure it out"
- Include chat history verbatim (summarize instead)
- Use relative file paths without explanation
- List files without explaining what changed
- Write vague next steps like "continue improving the code"

**✅ Do:**
- Write specific, actionable content for every section
- Explain the WHY behind decisions, not just WHAT was done
- Include code examples and command syntax
- Use absolute paths or clear relative path explanations
- Annotate file listings with modification status and purpose
- Define concrete next steps with acceptance criteria

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Don't know what timestamp to use | Use current timestamp when generating the file |
| Session had no meaningful work | Don't generate a context file - only create when there's substantial content |
| User worked on multiple unrelated things | Create separate sections for each major area of work |
| Don't know user's configuration | Ask user directly for their setup before generating |
| Project structure is complex | Use a tree diagram with annotations for key directories |
| Too much detail to include | Prioritize: completed work > pending work > analysis > nice-to-know |

## Validation Commands

Before declaring the context document complete:

```bash
# Verify file was created in correct location
ls -la restore-context/session-context-*.md

# Check file size (should be substantial, >10KB typically)
wc -l restore-context/session-context-*.md

# Preview first 50 lines to verify formatting
head -n 50 restore-context/session-context-*.md
```

---

**Related Skills:**
- Use **feedback-generator** to create improvement proposal documents
- Use **skills-index-updater** to register new skills after creation
