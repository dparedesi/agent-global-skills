# Agent Global Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/github/v/release/dparedesi/agent-global-skills)](https://github.com/dparedesi/agent-global-skills/releases)

<a href="https://buymeacoffee.com/dparedesi" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50"></a>

A collection of reusable AI agent skills for [Claude Code](https://claude.com/claude-code), Gemini, and other coding assistants - modular, prompt-based workflows that extend AI capabilities for specific tasks.

## What are Skills?

Skills are reusable prompts that AI coding assistants automatically discover and activate based on keyword triggers. Each skill lives in its own directory with a `SKILL.md` file containing YAML frontmatter (name, description) and detailed instructions.

## Available Skills (18)

### 📄 Document Processing
| Skill | Description | Trigger Examples |
|-------|-------------|------------------|
| **docx** | Create, edit, and analyze Word documents with tracked changes and comments | "create docx", "edit document" |
| **pdf** | Extract text/tables, create PDFs, merge/split, fill forms | "extract pdf", "fill pdf form" |
| **pptx** | Create and edit PowerPoint presentations | "create presentation", "edit pptx" |
| **xlsx** | Spreadsheet creation, formulas, data analysis, visualization | "create spreadsheet", "analyze excel" |

### 📧 Productivity
| Skill | Description | Trigger Examples |
|-------|-------------|------------------|
| **inbox-assistant** | AI-powered Gmail management - triage, cleanup, batch operations | "inbox", "email triage", "clean inbox" |
| **synap-assistant** | Personal knowledge capture - ideas, todos, projects, daily reviews | "synap", "brain dump", "capture this" |
| **save-context** | Generate session handoff documents for agent continuity | "save context", "handoff", "wrap up" |

### 🛠️ Development
| Skill | Description | Trigger Examples |
|-------|-------------|------------------|
| **elevate-code** | Transform projects to production quality using 12 proven patterns | "elevate-code", "production ready" |
| **commit-and-push** | Streamlined git workflow - analyze, commit, push, optionally PR | `/commit-and-push` |
| **cli-onboarding** | Patterns for CLI first-time UX (setup wizards, doctor commands) | "onboarding", "setup wizard" |

### 🤖 AI Tooling
| Skill | Description | Trigger Examples |
|-------|-------------|------------------|
| **skill-builder** | Create, evaluate, and improve skills to production quality | "create a new skill", "review skill" |
| **skill-feedback** | Capture session learnings for skill/package improvements | "skill-feedback", "capture improvements" |
| **skills-index-updater** | Regenerate AGENTS.md for IDEs without native skill support | "update skill index", "sync agents" |
| **skills-local-setup** | Create symlinks for multi-agent compatibility in repos | "setup skills", "configure agents" |

### 📊 Dashboards & Analytics
| Skill | Description | Trigger Examples |
|-------|-------------|------------------|
| **llms-dashboard** | Generate HTML dashboards for AI tool usage statistics | "visualize AI usage", "usage statistics" |
| **token-pacing** | Calculate optimal token burn rate to reach 100% by reset | "token budget", "will I run out" |

### 🔧 Utilities
| Skill | Description | Trigger Examples |
|-------|-------------|------------------|
| **mac-health** | Quick Mac system health check with actionable recommendations | "mac health", "battery check", "ram usage" |
| **humanize** | Make AI-written text read more naturally | "humanize", "sounds robotic", "make it natural" |
| **slack-gif-creator** | Create animated GIFs optimized for Slack | "make a GIF for Slack" |

## Skill Structure

Each skill follows a consistent pattern:

```
skill-name/
├── SKILL.md          # Main entry point with YAML frontmatter
├── REFERENCE.md      # (optional) Lookup tables, patterns
├── EXAMPLES.md       # (optional) Before/after comparisons
└── scripts/          # (optional) Supporting scripts
```

## Installation

```bash
git clone https://github.com/dparedesi/agent-global-skills.git ~/.claude/skills
cd ~/.claude/skills && ./setup.sh
```

## Usage

Skills are invoked automatically when your request matches their trigger keywords, or explicitly via slash command:

```
/commit-and-push
/elevate-code
/humanize
```

## Design Principles

- **Progressive Disclosure** - SKILL.md is the entry point; complexity lives in supporting files
- **Actionable Outputs** - Skills produce concrete results, not just information
- **Safety by Default** - Destructive operations require confirmation
- **Undo Capability** - Where applicable, operations can be reversed

## Cross-Agent Compatibility

These skills work with multiple AI coding assistants:
- **Claude Code** - Native support (auto-discovers `~/.claude/skills`)
- **Gemini/Kiro** - Run `/skills-local-setup` in your repo to create AGENTS.md symlinks
- **Other IDEs** - Use `/skills-index-updater` to regenerate indexes
