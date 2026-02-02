# Implementation Plan: TUI for Todo Manager

## Goal Description
Create an interactive Terminal User Interface (TUI) using the `textual` library to provide an "always-on" application experience. This will run alongside the existing CLI, sharing the same data.

## User Review Required
None.

## Proposed Changes

### Dependencies
#### [NEW] [requirements.txt](file:///C:/Users/vdala/OneDrive/Antigravity/aiagent-todo-manager/requirements.txt)
-   Add `textual>=0.47.1`

### Application Logic
#### [NEW] [tui.py](file:///C:/Users/vdala/OneDrive/Antigravity/aiagent-todo-manager/tui.py)
This will be the main entry point for the TUI application.
-   **App Class**: `TodoApp(App)`
-   **Layout**:
    -   **Header**: App Title + Current Date
    -   **Main**: Vertical scrollable container.
    -   **Task Lists**: Three `Collapsible` or `Static` widgets, one for each Eisenhower category.
    -   **Input**: A `Input` widget at the bottom for adding tasks quickly.
    -   **Footer**: Key bindings help (`q`: Quit, `n`: New, `Space`: Complete).
-   **Interactivity**:
    -   Click to toggle completion status.
    -   Auto-refresh on adding tasks.

#### [MODIFY] [storage.py](file:///C:/Users/vdala/OneDrive/Antigravity/aiagent-todo-manager/storage.py)
-   No major changes expected, but we need to ensure verify methods are robust for rapid reloading.

## Verification Plan

### Manual Verification
-   **Launch**: Run `python tui.py` and ensure it renders.
-   **Add Task**: Type in input box, press Enter, verify it appears in correct category.
-   **View**: Verify headers show correct counts and priorities.
-   **Interaction**: Click a task to complete it.
-   **Cross-Check**: Open a separate terminal, run `py todo.py list`, and verify data matches.
