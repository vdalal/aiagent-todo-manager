
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static, Label, Checkbox, Button
from textual.containers import Container, Vertical, Horizontal
from textual.binding import Binding
from textual import on

from storage import TaskStore
from task import Task, CAT_IMPORTANT_URGENT, CAT_URGENT, CAT_IMPORTANT
from week_utils import get_week_start
import argparse
import shlex

# Mapping for display
TITLE_MAP = {
    CAT_IMPORTANT_URGENT: "🔴 Important & Urgent (Priority 1)",
    CAT_URGENT: "🟠 Urgent (Priority 2)",
    CAT_IMPORTANT: "🔵 Important (Priority 3)"
}


class TaskWidget(Horizontal):
    """Display a single task with a completion checkbox."""
    def __init__(self, task):
        super().__init__()
        self.todo_task = task

    def compose(self) -> ComposeResult:
        # Checkbox for completion status
        cb = Checkbox(value=self.todo_task.completed, label=str(self.todo_task.text))
        cb.task_id = self.todo_task.id  # Attach ID to widget for easy access
        yield cb

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        # We handle logic in the App, but we can verify here if needed
        pass

class TodoApp(App):
    """The TUI Application."""
    
    CSS = """
    Screen {
        layout: vertical;
    }
    .header {
        dock: top;
        height: 3;
        content-align: center middle;
        background: $primary;
        color: white;
        text-style: bold;
    }
    .category-title {
        background: $accent;
        color: auto;
        padding: 0 1;
        margin-top: 1;
        text-style: bold;
    }
    #task-container {
        height: 1fr;
        border: solid green;
        overflow-y: auto;
    }
    Input {
        dock: bottom;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
    ]

    def __init__(self):
        super().__init__()
        self.store = TaskStore()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Vertical(id="task-container"):
            yield Label(TITLE_MAP[CAT_IMPORTANT_URGENT], classes="category-title")
            yield Vertical(id=f"list_{CAT_IMPORTANT_URGENT}")
            
            yield Label(TITLE_MAP[CAT_URGENT], classes="category-title")
            yield Vertical(id=f"list_{CAT_URGENT}")
            
            yield Label(TITLE_MAP[CAT_IMPORTANT], classes="category-title")
            yield Vertical(id=f"list_{CAT_IMPORTANT}")

        yield Input(placeholder="Add task... (e.g. 'Buy milk -c urgent')", id="input")
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_tasks()

    def refresh_tasks(self) -> None:
        """Reload tasks from storage and update UI."""
        week_start = get_week_start()
        tasks = self.store.get_tasks_for_week(week_start)
        
        # Sort tasks by ID (preserving creation order mostly)
        tasks.sort(key=lambda t: t.id)

        # Clear existing lists
        for cat in [CAT_IMPORTANT_URGENT, CAT_URGENT, CAT_IMPORTANT]:
            container = self.query_one(f"#list_{cat}", Vertical)
            container.remove_children()

        # Populate lists
        for task in tasks:
            # Skip invalid categories if any
            if task.category not in TITLE_MAP:
                continue
            
            container = self.query_one(f"#list_{task.category}", Vertical)
            container.mount(TaskWidget(task))

    @on(Input.Submitted)
    def add_task(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        if not text:
            return

        # Simple manual parsing to simulate CLI args
        # We expect: "Task text -c category"
        parts = text.split(" -c ")
        task_text = parts[0].strip()
        category = CAT_IMPORTANT_URGENT # Default
        
        if len(parts) > 1:
            cat_arg = parts[1].split()[0] # Take first word after -c
            # Normalize user input to category constants
            if cat_arg in ['urgent', 'u']:
                category = CAT_URGENT
            elif cat_arg in ['important', 'i']:
                category = CAT_IMPORTANT
            elif cat_arg in ['important_urgent', 'iu']:
                category = CAT_IMPORTANT_URGENT

        # Check limits (active tasks only)
        week_start = get_week_start()
        count = self.store.get_task_count_by_category(week_start, category)
        
        if count >= 3:
            self.notify(f"Category Full! (3 active tasks limit)", severity="error")
            return

        # Add task
        new_task = Task(task_text, category=category)
        self.store.add_task(new_task)
        
        # Clear input and refresh
        event.input.value = ""
        self.refresh_tasks()
        self.notify("Task Added!")

    @on(Checkbox.Changed)
    def on_task_completion(self, event: Checkbox.Changed) -> None:
        """Handle task completion toggles."""
        task_id = event.checkbox.task_id
        is_complete = event.value
        
        # Update storage
        tasks = self.store.load_tasks()
        for t in tasks:
            if t.id == task_id:
                t.completed = is_complete
                break
        self.store.save_tasks(tasks)
        
        # We don't necessarily need a full refresh here as the UI is already updated by the checkbox,
        # but a refresh ensures sort order or styling updates if we add them later.
        # For now, let's keep it simple and NOT refresh to avoid flickering, 
        # unless we move completed tasks to the bottom? 
        # The prompt didn't ask for sorting in TUI, but consistency is good.
        # Let's simple save.

if __name__ == "__main__":
    app = TodoApp()
    app.run()
