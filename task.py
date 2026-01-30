"""Task model for weekly task management system."""


from datetime import datetime
from week_utils import get_week_start



# Categories
CAT_IMPORTANT_URGENT = 'important_urgent'
CAT_URGENT = 'urgent'
CAT_IMPORTANT = 'important'

VALID_CATEGORIES = [CAT_IMPORTANT_URGENT, CAT_URGENT, CAT_IMPORTANT]

class Task:
    """Represents a single task with integer ID and Eisenhover category.

    Tasks are assigned to a category and current week. ID is a unique integer.
    """

    def __init__(self, text, category, task_id=None, completed=False, week_start=None, created_at=None):
        """Create a new task.

        Args:
            text: Task description
            category: One of 'important_urgent', 'urgent', 'important'
            task_id: Integer ID (assigned by store if None)
            completed: Whether task is completed (default False)
            week_start: ISO date string for Monday of week (auto-calculated if None)
            created_at: ISO datetime string (auto-generated if None)
        """
        if category not in VALID_CATEGORIES:
            raise ValueError(f"Invalid category. Must be one of: {', '.join(VALID_CATEGORIES)}")

        self.id = task_id  # Will be assigned by store if None
        self.text = text
        self.category = category
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
            'category': self.category,
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
            category=data.get('category', CAT_IMPORTANT), # Default for migration safety if needed
            task_id=data['id'],
            completed=data['completed'],
            week_start=data['week_start'],
            created_at=data['created_at']
        )
