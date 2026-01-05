# Claude Code Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<a href="https://buymeacoffee.com/dparedesi" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50"></a>


A personal collection of skills for [Claude Code](https://claude.com/claude-code) - modular, prompt-based workflows that extend Claude's capabilities for specific tasks.

## What are Skills?

Skills are reusable prompts that Claude Code automatically discovers and activates based on keyword triggers. Each skill lives in its own directory with a `SKILL.md` file containing YAML frontmatter (name, description) and detailed instructions.

## Available Skills

| Skill | Description | Trigger Examples |
|-------|-------------|------------------|
| **commit-and-push** | Streamlined git workflow - analyzes changes, creates commit message, pushes, optionally creates PR | `/commit-and-push` |
| **elevate-code** | Transform projects to production quality using 12 proven patterns | "elevate-code", "production ready", "make it production grade" |
| **humanize** | Make AI-written text read more naturally through targeted edits | "humanize", "sounds robotic", "make it natural" |
| **inbox-assistant** | AI-powered Gmail management - triage, cleanup, and batch operations | "inbox", "email triage", "clean inbox" |
| **llms-dashboard** | Generate HTML dashboards for AI tool usage statistics | "visualize AI usage", "usage statistics" |
| **save-context** | Generate session handoff documents for agent continuity | "save context", "handoff", "wrap up" |
| **skill-builder** | Create, evaluate, and improve skills to production quality | "create a new skill", "review skill" |
| **skill-feedback** | Capture session learnings for skill/package improvements | "skill-feedback", "capture improvements" |
| **skills-index-updater** | Regenerate AGENTS.md for IDEs without native skill support | "update skill index", "sync agents" |
| **skills-local-setup** | Create symlinks for multi-agent compatibility in repos | "setup skills", "configure agents" |
| **transcribe** | Transcribe audio with speaker diarization using VoxScriber | "transcribe", "meeting transcript" |
| **cli-onboarding** | Patterns for CLI first-time user experience (setup wizards, doctor commands) | "onboarding", "setup wizard" |

## Skill Structure

Each skill follows a consistent pattern:

```
skill-name/
├── SKILL.md          # Main entry point with YAML frontmatter
├── REFERENCE.md      # (optional) Lookup tables, patterns
├── EXAMPLES.md       # (optional) Before/after comparisons
└── scripts/          # (optional) Supporting scripts
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

## Other AI Tools

For AI IDE/CLIs without native skill support (Gemini/Antigravity, Kiro, etc.), run `/skills-local-setup` to create compatibility symlinks in your repository.
