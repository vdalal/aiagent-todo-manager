"""Task model for weekly task management system."""

import uuid
from datetime import datetime
from week_utils import get_week_start


class Task:
    """Represents a single task with auto-generated ID and week assignment.

    Tasks are automatically assigned to the current week (Monday-Sunday)
    when created. UUIDs ensure reliable identification for operations.
    """

    def __init__(self, text, completed=False, task_id=None, week_start=None, created_at=None):
        """Create a new task.

        Args:
            text: Task description
            completed: Whether task is completed (default False)
            task_id: UUID string (auto-generated if None)
            week_start: ISO date string for Monday of week (auto-calculated if None)
            created_at: ISO datetime string (auto-generated if None)
        """
        self.id = task_id if task_id else str(uuid.uuid4())
        self.text = text
        self.completed = completed
        self.week_start = week_start if week_start else get_week_start()
        self.created_at = created_at if created_at else datetime.now().isoformat()

    def to_dict(self):
        """Convert task to dictionary for JSON serialization.

        Returns:
            dict: Task data suitable for JSON storage
        """
        return {
            'id': self.id,
            'text': self.text,
            'completed': self.completed,
            'week_start': self.week_start,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        """Create task from dictionary loaded from JSON.

        Args:
            data: Dictionary with task fields

        Returns:
            Task: Reconstructed task object
        """
        return cls(
            text=data['text'],
            completed=data['completed'],
            task_id=data['id'],
            week_start=data['week_start'],
            created_at=data['created_at']
        )
