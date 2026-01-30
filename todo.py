import argparse
import sys
from task import Task, VALID_CATEGORIES, CAT_IMPORTANT_URGENT, CAT_URGENT, CAT_IMPORTANT
from storage import TaskStore
from week_utils import get_week_start

# Priority mapping (Lower is higher priority)
PRIORITY_MAP = {
    CAT_IMPORTANT_URGENT: 1,
    CAT_URGENT: 2,
    CAT_IMPORTANT: 3
}


DISPLAY_NAMES = {
    CAT_IMPORTANT_URGENT: "Important & Urgent (Priority 1)",
    CAT_URGENT: "Urgent (Priority 2)",
    CAT_IMPORTANT: "Important (Priority 3)"
}

def add_task(args, store):
    """Add a new task to the current week with category checks.

    Args:
        args: Parsed command arguments
        store: TaskStore instance

    Exits with code 1 on storage errors or validation failure.
    """
    try:
        current_week = get_week_start()
        
        # Check limit
        count = store.get_task_count_by_category(current_week, args.category)
        if count >= 3:
            print(f"Error: Category '{DISPLAY_NAMES[args.category]}' is full (3/3 tasks).")
            print("Complete or delete existing tasks in this category first.")
            sys.exit(1)

        task = Task(args.text, category=args.category)
        store.add_task(task)
        print(f"Added task: {task.text} (ID: {task.id}) -> {DISPLAY_NAMES[task.category]}")
    except IOError:
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


def list_tasks(args, store):
    """List all tasks for the current week sorted by priority.

    Args:
        args: Parsed command arguments
        store: TaskStore instance
    """
    try:
        current_week = get_week_start()
        tasks = store.get_tasks_for_week(current_week)

        if not tasks:
            print("No tasks for this week")
            return


        # Sort: Priority FIRST, then Completed status, then ID
        # This keeps completed tasks under their respective Category headers
        tasks.sort(key=lambda t: (PRIORITY_MAP.get(t.category, 99), t.completed, t.id))

        current_cat = None
        for task in tasks:
            # Print header if category changes
            if task.category != current_cat:
                current_cat = task.category
                print(f"\n--- {DISPLAY_NAMES.get(current_cat, current_cat)} ---")

            status = "~~" if task.completed else ""
            print(f"[{task.id}] {status}{task.text}{status}")
            
    except IOError:
        sys.exit(1)


def complete_task(args, store):
    """Mark a task as completed.

    Args:
        args: Parsed command arguments with id attribute (int)
        store: TaskStore instance
    """
    try:
        tasks = store.load_tasks()
        task = None
        for t in tasks:
            if t.id == args.id:
                task = t
                break

        if task is None:
            print(f"Task not found: {args.id}")
            sys.exit(1)

        task.completed = True
        store.save_tasks(tasks)
        print(f"Marked complete: {task.text}")
    except IOError:
        sys.exit(1)


def delete_task(args, store):
    """Delete a task from storage.

    Args:
        args: Parsed command arguments with id attribute (int)
        store: TaskStore instance
    """
    try:
        tasks = store.load_tasks()
        task = None
        for t in tasks:
            if t.id == args.id:
                task = t
                break

        if task is None:
            print(f"Task not found: {args.id}")
            sys.exit(1)

        tasks.remove(task)
        store.save_tasks(tasks)
        print(f"Deleted: {task.text}")
    except IOError:
        sys.exit(1)



def complete_all(args, store):
    """Mark all tasks in the current week as completed.

    Args:
        args: Parsed command arguments
        store: TaskStore instance
    """
    try:
        current_week = get_week_start()
        tasks = store.load_tasks()
        
        count = 0
        for task in tasks:
            if task.week_start == current_week and not task.completed:
                task.completed = True
                count += 1
        
        if count > 0:
            store.save_tasks(tasks)
            print(f"Marked {count} tasks as complete.")
        else:
            print("No active tasks to complete for this week.")
            
    except IOError:
        sys.exit(1)


def delete_all(args, store):
    """Delete all tasks in the current week.

    Args:
        args: Parsed command arguments
        store: TaskStore instance
    """
    try:
        current_week = get_week_start()
        tasks = store.load_tasks()
        
        # Keep tasks that are NOT in the current week
        remaining_tasks = [t for t in tasks if t.week_start != current_week]
        deleted_count = len(tasks) - len(remaining_tasks)
        
        if deleted_count > 0:
            store.save_tasks(remaining_tasks)
            print(f"Deleted {deleted_count} tasks from this week.")
        else:
            print("No tasks to delete for this week.")
            
    except IOError:
        sys.exit(1)


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Eisenhower Matrix Weekly Manager",
        prog="todo"
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('text', help='Task description')
    add_parser.add_argument('--category', '-c', 
                          choices=VALID_CATEGORIES, 
                          default=CAT_IMPORTANT_URGENT,
                          help='Task category (default: important_urgent)')

    # List command
    list_parser = subparsers.add_parser('list', help='List current week tasks')

    # Complete command
    complete_parser = subparsers.add_parser('complete', help='Mark task as complete')
    complete_parser.add_argument('id', type=int, help='Task ID to complete')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', type=int, help='Task ID to delete')

    # Bulk Operations
    subparsers.add_parser('complete-all', help='Mark ALL current week tasks as complete')
    subparsers.add_parser('delete-all', help='Delete ALL tasks for the current week')

    # Parse arguments
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    store = TaskStore()

    if args.command == 'add':
        add_task(args, store)
    elif args.command == 'list':
        list_tasks(args, store)
    elif args.command == 'complete':
        complete_task(args, store)
    elif args.command == 'delete':
        delete_task(args, store)
    elif args.command == 'complete-all':
        complete_all(args, store)
    elif args.command == 'delete-all':
        delete_all(args, store)


if __name__ == '__main__':
    main()
