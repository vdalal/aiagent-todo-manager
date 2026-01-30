# Verification Plan: Stability & Edge Cases

## Goal
Verify system stability, ensure no regressions in core functionality, and specifically test edge cases involving deletion and re-addition of tasks.

## Test Cases

### 1. Core Functionality (Regressions)
- [ ] **Add Task**: Add a task and verify it appears in the list.
- [ ] **Date Header**: Verify list output contains the date header.
- [ ] **Category Grouping**: Verify tasks are grouped by category.
- [ ] **Priority Sorting**: Verify high priority (Important & Urgent) appears before low priority.

### 2. ID Generation & Deletion Logic
- [ ] **Sequential IDs**: Add 3 tasks -> IDs should be 1, 2, 3.
- [ ] **Delete Middle**: Delete ID 2. List -> [1, 3].
- [ ] **Append after Delete**: Add new task. ID should be 4 (ID logic is based on max existing ID).
- [ ] **Delete Last**: Delete ID 4. List -> [1, 3].
- [ ] **Add after Delete Last**: Add new task. ID should be 4 (Max(1,3) + 1).

### 3. Empty State Reset
- [ ] **Delete All**: clear all tasks.
- [ ] **Add First Task**: Add new task. ID should be 1.

### 4. Category Limits (Strict Enforcement)
- [ ] **Fill Category**: Add 3 tasks to 'Urgent'.
- [ ] **Block Overflow**: Try adding 4th -> Fail.
- [ ] **Free Space**: Delete one 'Urgent' task.
- [ ] **Fill Space**: Add new 'Urgent' task -> Success.

## Execution
Run `verify_comprehensive.py` to automate these checks.
