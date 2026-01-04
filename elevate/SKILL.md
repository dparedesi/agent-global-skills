---
name: elevate
description: Elevate projects to production quality using proven patterns. Use when starting a project, reviewing architecture, auditing code, or when user mentions "elevate", "production ready", "patterns", "make it production grade", or "make it look like Sr. Distinguished Engineer".
---

# Elevate

*Transform any project into production-quality software using proven patterns.*

**The Problem**: Most projects fail in predictable ways—users can't set them up, accidents cause data loss, crashes waste hours of progress, code becomes unmaintainable, errors are cryptic. These aren't bugs; they're missing patterns.

**The Solution**: Elevate systematically applies 12 battle-tested patterns that distinguish amateur code from production software.

---

## Quick Start

| Mode | When to Use | What Happens |
|------|-------------|--------------|
| **New Project** | Starting from scratch | Detect type → Generate scaffold with all patterns |
| **Audit** | Reviewing existing code | Detect type → Scan → Gap report |
| **Transform** | Elevating existing project | Audit + Propose + Generate missing pieces |

---

## The Foundation: The Triad

Three non-negotiable properties. If your project lacks any of these, fix them first.

| Property | Pattern | Litmus Test |
|----------|---------|-------------|
| **Health** | [The Doctor](patterns/01-health-doctor.md) | Can a new user run `tool doctor` and know what's missing? |
| **Safety** | [The Safety Net](patterns/02-safety-net.md) | Can a mistake be undone in under 60 seconds? |
| **Resilience** | [The Statekeeper](patterns/03-resilience-statekeeper.md) | Can interrupted work resume without losing progress? |

*Setup should verify. Mistakes should undo. Crashes should resume.*

---

## All 12 Pattern Categories

| # | Pattern | Problem It Solves | Reference |
|---|---------|-------------------|-----------|
| 1 | **Health (Doctor)** | "It doesn't work on my machine" | [patterns/01-health-doctor.md](patterns/01-health-doctor.md) |
| 2 | **Safety (Safety Net)** | "I accidentally deleted everything" | [patterns/02-safety-net.md](patterns/02-safety-net.md) |
| 3 | **Resilience (Statekeeper)** | "It crashed and I lost all progress" | [patterns/03-resilience-statekeeper.md](patterns/03-resilience-statekeeper.md) |
| 4 | **Architecture** | "The code is a tangled mess" | [patterns/04-architecture.md](patterns/04-architecture.md) |
| 5 | **Data Models** | "What shape is this data?" | [patterns/05-data-models.md](patterns/05-data-models.md) |
| 6 | **Code Organization** | "Where does this code go?" | [patterns/06-code-organization.md](patterns/06-code-organization.md) |
| 7 | **Error Handling** | "It failed but I don't know why" | [patterns/07-error-handling.md](patterns/07-error-handling.md) |
| 8 | **Testing** | "I'm afraid to change anything" | [patterns/08-testing.md](patterns/08-testing.md) |
| 9 | **Build & Deploy** | "How do I ship this?" | [patterns/09-build-deploy.md](patterns/09-build-deploy.md) |
| 10 | **CLI UX** | "This tool is confusing" | [patterns/10-cli-ux.md](patterns/10-cli-ux.md) |
| 11 | **Documentation** | "How does this work?" | [patterns/11-documentation.md](patterns/11-documentation.md) |
| 12 | **State Persistence** | "Where did my data go?" | [patterns/12-state-persistence.md](patterns/12-state-persistence.md) |

---

## Elevation Workflow

When you invoke `/elevate`, follow these 5 steps:

### Step 1: Detect Project Type

Scan for file markers to identify project type:

| File Markers | Project Type | Checklist |
|--------------|--------------|-----------|
| `pyproject.toml` + `[project.scripts]` | Python CLI | [checklists/python-cli.md](checklists/python-cli.md) |
| `package.json` + `"bin"` field | Node.js CLI | [checklists/node-cli.md](checklists/node-cli.md) |
| `manifest.json` + `"background"` | Browser Extension | [checklists/browser-extension.md](checklists/browser-extension.md) |
| `pyproject.toml` + `fastapi` in deps | REST API (Python) | [checklists/rest-api.md](checklists/rest-api.md) |
| `package.json` + `express`/`hono`/`fastify` | REST API (Node) | [checklists/rest-api.md](checklists/rest-api.md) |
| `mcp.json` OR `@modelcontextprotocol` imports | MCP Server | [checklists/mcp-server.md](checklists/mcp-server.md) |
| `action.yml` or `action.yaml` | GitHub Action | [checklists/github-action.md](checklists/github-action.md) |

### Step 2: Scan Existing Patterns

For each pattern category, grep for indicators:

```
Pattern Indicators:
- Doctor:     "doctor", "check", "verify", "preflight", "setup"
- Safety:     "undo", "restore", "trash", "backup", "dry-run", "soft.?delete"
- State:      "checkpoint", "resume", "state.json", "cursor", "progress"
- Data:       "@dataclass", "interface", "TypedDict", "Pydantic", "zod"
- Testing:    "pytest", "vitest", "jest", "conftest", "*.test.ts", "test_*.py"
- Errors:     "retry", "backoff", "graceful", "try.*except", "catch"
```

Score each pattern:
- **Present** — Pattern implemented correctly
- **Partial** — Some elements exist but incomplete
- **Missing** — No evidence of pattern

### Step 3: Generate Gap Report

```markdown
## Gap Analysis: <project-name>

**Project Type**: <detected-type>
**Patterns Detected**: X/12

### Present (Good)
- [x] Pattern Name - evidence found

### Partial (Needs Work)
- [~] Pattern Name - what exists, what's missing

### Missing (Critical)
- [ ] Pattern Name - why it matters for this project
```

### Step 4: Propose Transformations

For each gap, propose specific changes:

```markdown
## Proposed Transformations

### Priority 1: <Pattern> (Missing)
- Files to create
- Changes to existing files
- Code snippets

### Priority 2: <Pattern> (Partial)
- What to enhance
- Missing pieces
```

Prioritize by impact:
1. **Triad first** (Doctor, Safety, Statekeeper)
2. **Data Models** (foundation for everything else)
3. **Error Handling** (user experience)
4. **Testing** (confidence to change)
5. **Everything else**

### Step 5: Generate Scaffold

For missing patterns, generate files from templates:

- Use templates from `templates/<project-type>/`
- Customize with project name and existing patterns
- Show diff preview before writing

---

## Project Type Checklists

Comprehensive validation lists for each project type:

| Project Type | Checklist | Key Focus Areas |
|--------------|-----------|-----------------|
| Python CLI | [checklists/python-cli.md](checklists/python-cli.md) | pyproject.toml, src layout, argparse/click, rich |
| Node.js CLI | [checklists/node-cli.md](checklists/node-cli.md) | package.json, commander, ESM/CJS, chalk |
| Browser Extension | [checklists/browser-extension.md](checklists/browser-extension.md) | manifest v3, service workers, IndexedDB |
| REST API | [checklists/rest-api.md](checklists/rest-api.md) | FastAPI/Express, 12-factor, middleware |
| MCP Server | [checklists/mcp-server.md](checklists/mcp-server.md) | Tool definitions, context, resources |
| GitHub Action | [checklists/github-action.md](checklists/github-action.md) | action.yml, inputs/outputs, composite |

---

## Success Criteria

A fully elevated project should pass all checks:

- [ ] **Triad Litmus Test**: doctor ✓, undo ✓, resume ✓
- [ ] **Type Safety**: All data structures are typed (dataclass/interface)
- [ ] **Module Separation**: One module = one responsibility
- [ ] **Error Messages**: Include what failed + why + how to fix
- [ ] **Test Infrastructure**: Mocked external deps, fixtures, >80% coverage on core
- [ ] **Build Config**: Standard tooling (pyproject.toml / package.json)
- [ ] **AI Collaboration**: CLAUDE.md with architecture and patterns
- [ ] **Output Modes**: Human-readable + `--json` + `--quiet`

---

## Quick Audit (30 seconds)

Rapidly assess any project:

```bash
# Check for Triad patterns
grep -rE "(doctor|check|verify)" . | head -3      # Health
grep -rE "(undo|restore|dry-run)" . | head -3     # Safety
grep -rE "(checkpoint|resume|state)" . | head -3  # Resilience

# Check for type safety
grep -rE "(@dataclass|interface |TypedDict)" . | head -3

# Check for tests
find . -name "test_*.py" -o -name "*.test.ts" | head -3
```

No matches in a category = gap to address.

---

*Elevate: Because production-quality isn't about perfection—it's about patterns.*
