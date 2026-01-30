"""JSON-based task storage with error handling."""

import json
import os
from task import Task


class TaskStore:
    """Manages persistent storage of tasks in JSON format.

    Handles file read/write errors gracefully with clear error messages.
    Tasks are stored in a JSON file with structure: {"tasks": [...]}
    """

    def __init__(self, filepath='tasks.json'):
        """Initialize task storage.

        Args:
            filepath: Path to JSON file for task storage
        """
        self.filepath = filepath

    def load_tasks(self):
        """Load tasks from JSON file.

        Returns:
            list: List of Task objects, empty list if file doesn't exist

        Handles:
            - FileNotFoundError: Returns empty list
            - JSONDecodeError: Prints error message and returns empty list
        """
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                tasks = [Task.from_dict(task_data) for task_data in data.get('tasks', [])]
                return tasks
        except FileNotFoundError:
            # File doesn't exist yet - this is normal on first run
            return []
        except json.JSONDecodeError:
            print(f"Error: {self.filepath} is corrupted")
            return []

    def save_tasks(self, tasks):
        """Save tasks to JSON file.

        Args:
            tasks: List of Task objects to save

        Handles:
            - IOError: Prints error message about write permissions
        """
        try:
            data = {
                'tasks': [task.to_dict() for task in tasks]
            }
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error: Cannot write to {self.filepath} - check permissions")
            raise


    def add_task(self, task):
        """Add a new task to storage.

        Auto-assigns the next integer ID.

        Args:
            task: Task object to add
        """
        tasks = self.load_tasks()
        
        # Auto-increment ID
        if not tasks:
            next_id = 1
        else:
            # Find max existing ID (handles potentially unsorted lists)
            max_id = max(t.id for t in tasks)
            next_id = max_id + 1
        
        task.id = next_id
        tasks.append(task)
        self.save_tasks(tasks)

    def get_tasks_for_week(self, week_start):
        """Get all tasks for a specific week.

        Args:
            week_start: ISO date string for Monday of the week

        Returns:
            list: Task objects assigned to the specified week
        """
        tasks = self.load_tasks()
        return [task for task in tasks if task.week_start == week_start]

    def get_task_count_by_category(self, week_start, category):
        """Count tasks in a specific category for a given week.
        
        Args:
            week_start: ISO date string for Monday of the week
            category: Category string to count
            
        Returns:
            int: Number of tasks
        """
        tasks = self.get_tasks_for_week(week_start)
        return sum(1 for t in tasks if t.category == category)
