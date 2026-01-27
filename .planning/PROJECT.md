# CLI TODO Manager

## What This Is

A command-line TODO list manager in Python that organizes tasks by week (Monday-Sunday). Users can add tasks to the current week, view this week's tasks, mark tasks as complete (shown as crossed off), and delete tasks. All data is stored in a JSON file.

## Core Value

Users can quickly manage their weekly tasks from the command line without any external dependencies or setup complexity.

## Requirements

### Validated

- ✓ User can add new tasks to the current week — v1.0
- ✓ User can list all tasks for the current week — v1.0
- ✓ User can mark tasks as complete (shown crossed off with ~~text~~) — v1.0
- ✓ User can delete tasks by ID — v1.0
- ✓ Tasks are stored in a JSON file — v1.0
- ✓ Tasks have auto-generated IDs (UUID-based) — v1.0
- ✓ Week starts on Monday — v1.0
- ✓ Invalid commands show usage help — v1.0
- ✓ Invalid task IDs show error message — v1.0
- ✓ File read/write errors are caught and reported — v1.0

### Active

(None — v1.0 complete. Define new requirements for next milestone.)

### Out of Scope

- Priorities — keeping it simple, no task prioritization
- Due dates — weekly organization only, no specific dates
- Categories/tags — no task categorization
- Past week viewing — only current week is shown
- Multi-week planning — tasks only added to current week
- External dependencies — Python standard library only

## Context

**Current State (v1.0 shipped 2026-01-26):**
- 616 lines of Python across 5 modules
- Tech stack: Python 3.x with standard library only (uuid, datetime, json, argparse)
- All 15 v1 requirements validated through integration tests and human verification
- Zero known issues or technical debt

**History:**
This is a learning project to explore GSD workflow. The focus is on simplicity and reliability - a straightforward CLI tool that does one thing well: manage this week's tasks.

## Constraints

- **Tech stack**: Python standard library only — no external dependencies
- **Interface**: Command-line arguments (e.g., `python todo.py add "Buy milk"`)
- **Storage**: JSON file format
- **Complexity**: Keep it simple - basic task management without advanced features

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Week-based organization | Tasks naturally fit into weekly cycles | ✓ Good (v1.0) |
| UUID-based task IDs | More reliable than sequential numbers, no collision risk | ✓ Good (v1.0) |
| Show completed tasks crossed off | Users can see what they've accomplished this week | ✓ Good (v1.0 - ~~text~~ format) |
| Python standard library only | Zero setup, maximum portability | ✓ Good (v1.0 - achieved) |
| Monday-Sunday week boundaries | Aligns with ISO 8601 week definition | ✓ Good (v1.0) |
| JSON wrapper object structure | Allows future extension with metadata | ✓ Good (v1.0 - extensible) |
| Argparse with subparsers | Clean command structure with auto help | ✓ Good (v1.0) |
| Error handling returns empty list | FileNotFoundError is normal on first run | ✓ Good (v1.0) |

---
*Last updated: 2026-01-26 after v1.0 milestone*
