# Implementation Plan: Web UI Enhancements

## Goal Description
Enhance the Web GUI with:
1.  **Task Text Editing** (Completed)
2.  **Drag-and-Drop** (Completed)
3.  **Direct Task Addition**: Allow users to add tasks directly to a specific category via a "+" button in the quadrant header.
4.  **UI Cleanup**: Remove the redundant top "Add Task" bar.

## User Review Required
> [!NOTE]
> Selected Option 1: Header "+" Button.

## Proposed Changes

### Frontend
#### [MODIFY] [templates/index.html](file:///C:/Users/vdala/OneDrive/Antigravity/aiagent-todo-manager/templates/index.html)
-   **Add Task Button**:
    -   Add a small `+` button to each `.quadrant-header`.
    -   On click, insert a temporary input field at the *top* of the corresponding `.task-list`.
    -   On `Enter` in that input:
        -   Call `POST /api/tasks` with the specific category.
        -   Remove input and prepend the new task card.
    -   On `Blur` or `Escape`: remove the input without saving.
-   **Remove Top Bar**:
    -   Remove the `.add-task-container` form from `index.html`.
    -   Remove/Clean up associated CSS in `style.css`.
    -   Remove associated JS event listener in `index.html`.

#### [MODIFY] [static/style.css](file:///C:/Users/vdala/OneDrive/Antigravity/aiagent-todo-manager/static/style.css)
-   Style the `.add-btn` in the header (subtle, consistent with existing buttons).
-   Style the temporary input field to look like a task card being created.

## Verification Plan

### Manual Verification
1.  **Direct Add**:
    -   Click "+" in "Do First".
    -   Type "New Urgent Task" and hit Enter.
    -   Verify it appears at the top of "Do First".
    -   Verify it persists after reload.
2.  **Cancel Add**:
    -   Click "+".
    -   Press Escape or click away.
    -   Verify no task is created.
