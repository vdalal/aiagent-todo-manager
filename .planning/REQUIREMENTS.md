# Requirements: CLI TODO Manager

**Defined:** 2026-01-26
**Core Value:** Users can quickly manage their weekly tasks from the command line without any external dependencies or setup complexity.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### CLI Interface

- [ ] **CLI-01**: User can add tasks via `python todo.py add "task text"`
- [ ] **CLI-02**: User can list tasks via `python todo.py list`
- [ ] **CLI-03**: User can mark tasks complete via `python todo.py complete <id>`
- [ ] **CLI-04**: User can delete tasks via `python todo.py delete <id>`
- [ ] **CLI-05**: Invalid commands show usage help

### Task Management

- [ ] **TASK-01**: Tasks have auto-generated IDs
- [ ] **TASK-02**: Completed tasks are displayed crossed off in list view
- [ ] **TASK-03**: Tasks are organized by week (Monday-Sunday)
- [ ] **TASK-04**: New tasks are added to current week
- [ ] **TASK-05**: List command shows only current week's tasks

### Storage

- [ ] **STOR-01**: Tasks are persisted in a JSON file
- [ ] **STOR-02**: File read errors are caught and reported
- [ ] **STOR-03**: File write errors are caught and reported

### Error Handling

- [ ] **ERR-01**: Invalid task IDs show clear error message
- [ ] **ERR-02**: All file I/O operations handle errors gracefully

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Future Enhancements

- **FUT-01**: View past weeks' tasks
- **FUT-02**: Task priorities
- **FUT-03**: Due dates within the week
- **FUT-04**: Task categories/tags

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Priorities | Keeping it simple - basic task management only |
| Due dates | Weekly organization is sufficient for v1 |
| Categories/tags | Adds complexity, not core to weekly task management |
| External dependencies | Python standard library only for maximum portability |
| Multi-week planning | Current week focus keeps the tool simple |
| Task editing | Can delete and re-add for v1 |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| CLI-01 | Phase 2 | Pending |
| CLI-02 | Phase 2 | Pending |
| CLI-03 | Phase 2 | Pending |
| CLI-04 | Phase 2 | Pending |
| CLI-05 | Phase 2 | Pending |
| TASK-01 | Phase 1 | Complete |
| TASK-02 | Phase 2 | Pending |
| TASK-03 | Phase 1 | Complete |
| TASK-04 | Phase 2 | Pending |
| TASK-05 | Phase 2 | Pending |
| STOR-01 | Phase 1 | Complete |
| STOR-02 | Phase 1 | Complete |
| STOR-03 | Phase 1 | Complete |
| ERR-01 | Phase 2 | Pending |
| ERR-02 | Phase 1 | Complete |

**Coverage:**
- v1 requirements: 15 total
- Mapped to phases: 15
- Unmapped: 0

---
*Requirements defined: 2026-01-26*
*Last updated: 2026-01-26 after Phase 1 completion*
