# Roadmap: CLI TODO Manager

## Overview

This roadmap delivers a command-line TODO manager in two phases. Phase 1 establishes the foundation with JSON storage and week-based task organization. Phase 2 builds the complete CLI interface for managing tasks. The result is a simple, reliable tool for managing weekly tasks from the command line.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Core Storage & Task Model** - JSON persistence and week-based task structure
- [ ] **Phase 2: CLI Operations** - Command interface for add, list, complete, delete

## Phase Details

### Phase 1: Core Storage & Task Model
**Goal**: Establish reliable JSON-based task storage with week-based organization
**Depends on**: Nothing (first phase)
**Requirements**: STOR-01, STOR-02, STOR-03, TASK-01, TASK-03, ERR-02
**Success Criteria** (what must be TRUE):
  1. Tasks are persisted to a JSON file with auto-generated IDs
  2. Tasks are organized by week boundaries (Monday-Sunday)
  3. File read errors are caught and reported with clear messages
  4. File write errors are caught and reported with clear messages
  5. Task data can be loaded from the JSON file on subsequent runs
**Plans**: 2 plans

Plans:
- [ ] 01-01-PLAN.md — Foundation modules (Task model, week utilities, storage layer)
- [ ] 01-02-PLAN.md — Integration testing and verification

### Phase 2: CLI Operations
**Goal**: Provide complete command-line interface for managing weekly tasks
**Depends on**: Phase 1
**Requirements**: CLI-01, CLI-02, CLI-03, CLI-04, CLI-05, TASK-02, TASK-04, TASK-05, ERR-01
**Success Criteria** (what must be TRUE):
  1. User can add tasks via `python todo.py add "task text"`
  2. User can list current week's tasks via `python todo.py list`
  3. User can mark tasks complete via `python todo.py complete <id>` (displayed crossed off)
  4. User can delete tasks via `python todo.py delete <id>`
  5. Invalid commands show usage help
  6. Invalid task IDs show clear error messages
**Plans**: TBD

Plans:
- [ ] (Plans to be created during plan-phase)

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Core Storage & Task Model | 0/2 | Ready to execute | - |
| 2. CLI Operations | 0/? | Not started | - |

---
*Roadmap created: 2026-01-26*
*Last updated: 2026-01-26 after Phase 1 planning*
