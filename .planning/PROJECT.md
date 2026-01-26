# CLI TODO Manager

## What This Is

A command-line TODO list manager in Python that organizes tasks by week (Monday-Sunday). Users can add tasks to the current week, view this week's tasks, mark tasks as complete (shown as crossed off), and delete tasks. All data is stored in a JSON file.

## Core Value

Users can quickly manage their weekly tasks from the command line without any external dependencies or setup complexity.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] User can add new tasks to the current week
- [ ] User can list all tasks for the current week
- [ ] User can mark tasks as complete (shown crossed off)
- [ ] User can delete tasks by ID
- [ ] Tasks are stored in a JSON file
- [ ] Tasks have auto-generated IDs
- [ ] Week starts on Monday
- [ ] Invalid commands show usage help
- [ ] Invalid task IDs show error message
- [ ] File read/write errors are caught and reported

### Out of Scope

- Priorities — keeping it simple, no task prioritization
- Due dates — weekly organization only, no specific dates
- Categories/tags — no task categorization
- Past week viewing — only current week is shown
- Multi-week planning — tasks only added to current week
- External dependencies — Python standard library only

## Context

This is a learning project to explore GSD workflow. The focus is on simplicity and reliability - a straightforward CLI tool that does one thing well: manage this week's tasks.

## Constraints

- **Tech stack**: Python standard library only — no external dependencies
- **Interface**: Command-line arguments (e.g., `python todo.py add "Buy milk"`)
- **Storage**: JSON file format
- **Complexity**: Keep it simple - basic task management without advanced features

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Week-based organization | Tasks naturally fit into weekly cycles | — Pending |
| Auto-generated IDs | More reliable than text matching for operations | — Pending |
| Show completed tasks crossed off | Users can see what they've accomplished this week | — Pending |
| Python standard library only | Zero setup, maximum portability | — Pending |

---
*Last updated: 2026-01-26 after initialization*
