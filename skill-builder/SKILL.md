---
name: building-agent-skills
description: Create, evaluate, and improve Agent skills to production quality (100/100). Use when the user wants to create a new skill, review an existing skill, score a skill against best practices, or improve a skill's quality. Also use when the user mentions skill development, skill templates, or skill optimization.
---

# Skill Builder Workflow

Create, evaluate, and improve Agent skills to production quality.

## Quick Start

| Mode | When to Use | Starting Step |
|------|-------------|---------------|
| **Create** | Building a new skill from scratch | Step 1 |
| **Evaluate** | Scoring an existing skill | Step 4 |
| **Improve** | Upgrading a skill to 100/100 | Step 5 |

## Skill Files

| File | Purpose |
|------|---------|
| `SKILL.md` | This workflow |
| `SCORING.md` | Structure + Efficacy rubrics (MUST READ before scoring) |
| `TEMPLATES.md` | Starter templates and patterns (MUST READ before creating) |
| `EXAMPLES.md` | Before/after improvement examples |
| `CHECKLIST.md` | 50-point validation checklist |

---

## Mode 1: Create a New Skill

### Step 1: Gather Requirements

Ask the user:
1. **What does the skill do?** (core capability)
2. **When should it activate?** (trigger contexts)
3. **What tools/scripts are needed?** (dependencies)
4. **What's the expected output?** (deliverables)

### Step 2: Choose Skill Structure

> [!IMPORTANT]
> **Read [TEMPLATES.md](TEMPLATES.md)** before choosing. It contains starter templates and common patterns (Workflow, Reference, Generator).

| Complexity | Structure |
|------------|-----------|
| Simple | `SKILL.md` only |
| Standard | `SKILL.md` + `REFERENCE.md` + `EXAMPLES.md` |
| Complex | Above + `TESTING.md` + `scripts/` |

### Step 3: Write the SKILL.md

Use templates from [TEMPLATES.md](TEMPLATES.md). Ensure:
1. **Frontmatter** — valid YAML with `name` (gerund form) and `description`
2. **Description** — includes BOTH what it does AND when to use it
3. **Workflow** — clear, numbered steps
4. **Progressive disclosure** — link to supporting files

> [!TIP]
> Description is critical for discovery. Include multiple trigger keywords.

After creating, proceed to **Step 4** to evaluate.

---

## Mode 2: Evaluate an Existing Skill

### Step 4: Score the Skill

> [!CRITICAL]
> **Read [SCORING.md](SCORING.md) completely** before scoring. It contains both rubrics and scoring worksheets.

**Process:**
1. Read all skill files (SKILL.md + supporting files)
2. Score **Structure** (0-100): 9 categories — documentation completeness
3. Score **Efficacy** (0-100): 6 categories — actual effectiveness
4. Use Combined Score Matrix in SCORING.md for verdict
5. Identify gaps in both dimensions

**Present results using the format in [SCORING.md](SCORING.md#scoring-worksheet).**

If either score < 90, proceed to **Step 5**.

---

## Mode 3: Improve to 100/100

### Step 5: Plan Improvements

Based on evaluation, prioritize:

| Priority | Fixes | Target |
|----------|-------|--------|
| **P1 Critical** | Missing frontmatter, invalid YAML, empty description | Required to function |
| **P2 Important** | Missing triggers, no examples, no progressive disclosure | Required for 95+ |
| **P3 Polish** | Missing troubleshooting, no quick start, terminology issues | Required for 100 |

### Step 6: Execute Improvements

> [!CAUTION]
> **Get user approval before making changes.** Present the plan and wait for confirmation.

Work systematically:
1. Fix frontmatter first (skill won't load without valid YAML)
2. Enhance description with trigger keywords
3. Add progressive disclosure if SKILL.md > 200 lines
4. Create supporting files as needed
5. Add quality sections (Troubleshooting, Quick Start)

### Step 7: Verify Final Score

1. Re-read all skill files
2. Re-score against both rubrics
3. Confirm scores meet target
4. Present final structure and summary

---

## Validation Checklist (Quick)

Before declaring complete:
- [ ] `name` uses gerund form (verb + -ing)
- [ ] `description` includes what AND when
- [ ] SKILL.md under 500 lines
- [ ] Examples show concrete input/output
- [ ] Consistent terminology throughout

Full checklist: **[CHECKLIST.md](CHECKLIST.md)**

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Skill not discovered | Check description has trigger keywords |
| Low Structure score | Add missing sections per SCORING.md rubric |
| Low Efficacy score | Simplify — skill may be doing too many things |
| Frontmatter errors | Validate YAML syntax, check for reserved words |
| User confused by skill | Add Quick Start, improve decision density |

---

## Reference

- **[SCORING.md](SCORING.md)** — Structure + Efficacy rubrics with worksheets
- **[TEMPLATES.md](TEMPLATES.md)** — Starter templates and common patterns
- **[EXAMPLES.md](EXAMPLES.md)** — Before/after improvement examples
- **[CHECKLIST.md](CHECKLIST.md)** — 50-point validation checklist
