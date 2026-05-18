# Import BaseTask class and logging decorator from another module
from models.base_task import BaseTask, log_action


# Allowed priority levels for tasks
VALID_PRIORITIES = {"low", "medium", "high", "critical"}


# Child class that extends BaseTask with priority and category features
class PriorityTask(BaseTask):

    def __init__(
        self,
        title: str,
        priority: str = "medium",
        category: str = "general"
    ):

        # Call parent class constructor
        super().__init__(title)

        # Validate priority value
        if priority.lower() not in VALID_PRIORITIES:
            raise ValueError(
                f"Priority must be one of: {VALID_PRIORITIES}"
            )

        # Store priority and category
        self._priority = priority.lower()
        self._category = category.strip()

    # Getter for priority
    @property
    def priority(self):
        return self._priority

    # Getter for category
    @property
    def category(self):
        return self._category

    @log_action
    def change_priority(self, new_priority: str):

        # Validate new priority before updating
        if new_priority.lower() not in VALID_PRIORITIES:
            raise ValueError(f"Invalid priority: {new_priority}")

        # Update priority
        self._priority = new_priority.lower()

    def priority_score(self) -> int:

        # Convert text priority into numeric score
        # Useful for sorting tasks by importance
        scores = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4
        }

        return scores.get(self._priority, 0)

    def to_dict(self) -> dict:

        # Convert object data into dictionary format
        data = super().to_dict()

        data.update({
            "priority": self._priority,
            "category": self._category,
            "type": "priority"
        })

        return data

    def __str__(self):

        # Task completion status
        status = "✓" if self._completed else "○"

        # Icons for different priority levels
        priority_icons = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🟠",
            "critical": "🔴"
        }

        icon = priority_icons.get(self._priority, "⚪")

        # User-friendly task display format
        return (
            f"[{status}] #{self._task_id} "
            f"{icon} [{self._priority.upper()}] "
            f"{self._title} "
            f"(Category: {self._category})"
        )


# Child class for tasks with deadlines
class DeadlineTask(PriorityTask):

    def __init__(
        self,
        title: str,
        deadline: str,
        priority: str = "high",
        category: str = "deadline"
    ):

        # Initialize parent class attributes
        super().__init__(title, priority, category)

        # Validate deadline format
        if not self._validate_deadline(deadline):
            raise ValueError(
                "Deadline must be in YYYY-MM-DD format."
            )

        # Store deadline
        self._deadline = deadline

    @staticmethod
    def _validate_deadline(deadline: str) -> bool:

        # Import regex module locally
        import re

        # Check if deadline matches YYYY-MM-DD format
        return bool(
            re.match(r'^\d{4}-\d{2}-\d{2}$', deadline)
        )

    # Getter for deadline
    @property
    def deadline(self):
        return self._deadline

    def to_dict(self) -> dict:

        # Extend parent dictionary with deadline data
        data = super().to_dict()

        data.update({
            "deadline": self._deadline,
            "type": "deadline"
        })

        return data

    def __str__(self):

        # Get formatted string from parent class
        base = super().__str__()

        # Add deadline information
        return f"{base}  ⏰ Due: {self._deadline}"