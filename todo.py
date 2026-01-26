"""Command-line interface for weekly task management.

Provides add, list, complete, and delete operations with proper error handling.
"""

import argparse
import sys
from task import Task
from storage import TaskStore
from week_utils import get_week_start


def add_task(args, store):
    """Add a new task to the current week.

    Args:
        args: Parsed command arguments with text attribute
        store: TaskStore instance for persistence

    Exits with code 1 on storage errors.
    """
    try:
        task = Task(args.text)
        store.add_task(task)
        print(f"Added task: {task.text} (ID: {task.id})")
    except IOError:
        sys.exit(1)


def list_tasks(args, store):
    """List all tasks for the current week.

    Displays incomplete tasks as: [ID] text
    Displays completed tasks as: [ID] ~~text~~

    Args:
        args: Parsed command arguments (unused)
        store: TaskStore instance for persistence

    Exits with code 1 on storage errors.
    """
    try:
        current_week = get_week_start()
        tasks = store.get_tasks_for_week(current_week)

        if not tasks:
            print("No tasks for this week")
            return

        for task in tasks:
            if task.completed:
                print(f"[{task.id}] ~~{task.text}~~")
            else:
                print(f"[{task.id}] {task.text}")
    except IOError:
        sys.exit(1)


def complete_task(args, store):
    """Mark a task as completed.

    Args:
        args: Parsed command arguments with id attribute
        store: TaskStore instance for persistence

    Exits with code 1 if task ID not found or on storage errors.
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
        args: Parsed command arguments with id attribute
        store: TaskStore instance for persistence

    Exits with code 1 if task ID not found or on storage errors.
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


def main():
    """Main entry point for CLI.

    Sets up argument parser with subcommands and routes to handlers.
    """
    parser = argparse.ArgumentParser(
        description="Weekly task management CLI",
        prog="todo"
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('text', help='Task description')

    # List command
    list_parser = subparsers.add_parser('list', help='List current week tasks')

    # Complete command
    complete_parser = subparsers.add_parser('complete', help='Mark task as complete')
    complete_parser.add_argument('id', help='Task ID to complete')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', help='Task ID to delete')

    # Parse arguments
    args = parser.parse_args()

    # Show help if no command specified
    if args.command is None:
        parser.print_help()
        sys.exit(0)

    # Initialize storage
    store = TaskStore()

    # Route to command handlers
    if args.command == 'add':
        add_task(args, store)
    elif args.command == 'list':
        list_tasks(args, store)
    elif args.command == 'complete':
        complete_task(args, store)
    elif args.command == 'delete':
        delete_task(args, store)


if __name__ == '__main__':
    main()
