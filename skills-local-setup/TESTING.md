# Testing Scenarios

## Scenario 1: Fresh Repository

**Setup**: New repo with `AGENTS.md` and `.agent/` directory, no existing symlinks.

**Command**: `./scripts/setup-local-skills.sh all`

**Expected**:
- Creates `GEMINI.md -> AGENTS.md`
- Creates `.claude/skills -> ../.agent/skills`
- Adds entries to `.gitignore`
- Exit code 0

**Failure Indicators**: Script errors, absolute paths in symlinks, missing .gitignore entries

---

## Scenario 2: Existing Files (Conflict)

**Setup**: Repo with existing `.claude/` directory containing real files.

**Command**: `./scripts/setup-local-skills.sh claude`

**Expected**:
- Shows current contents of `.claude/`
- Prompts "Do you want to remove... [y/N]"
- If Y: removes and creates symlink
- If N: skips and continues

**Failure Indicators**: Overwrites without asking, crashes on existing files

---

## Scenario 3: Missing Prerequisites

**Setup**: Not in a git repo, or missing `AGENTS.md`.

**Command**: `./scripts/setup-local-skills.sh gemini`

**Expected**:
- Prints clear error message
- Exit code 1
- No partial changes made

**Failure Indicators**: Creates broken symlinks, no error message, exit code 0

---

## Model Coverage

Tested with: Sonnet, Opus
