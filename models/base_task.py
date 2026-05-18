import re
from datetime import datetime


# Decorator for logging method calls with current timestamp
def log_action(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        # Get current date and time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Print log message after function execution
        print(f"  [LOG {timestamp}] {func.__name__} called.")

        return result
    return wrapper


# Base class representing a generic task in the To Do List Manager
class BaseTask:

    # Class variable used to automatically assign unique IDs
    _id_counter = 1

    def __init__(self, title: str):

        # Validate task title before creating task
        if not self._validate_title(title):
            raise ValueError(
                "Task title must be a non-empty string (letters/numbers only)."
            )

        # Private attributes (encapsulation)
        self._task_id = BaseTask._id_counter
        BaseTask._id_counter += 1

        self._title = title.strip()
        self._completed = False

        # Store task creation time
        self._created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _validate_title(title: str) -> bool:

        # Regex pattern allows letters, numbers, spaces and simple symbols
        pattern = r'^[\w\s,.!?\-()]{1,100}$'

        # Returns True if title matches pattern
        return bool(re.match(pattern, title.strip()))

    # Getter for task ID
    @property
    def task_id(self):
        return self._task_id

    # Getter for task title
    @property
    def title(self):
        return self._title

    # Getter for completion status
    @property
    def completed(self):
        return self._completed

    # Getter for creation date
    @property
    def created_at(self):
        return self._created_at

    @log_action
    def mark_complete(self):

        # Mark task as completed
        self._completed = True

    @log_action
    def mark_incomplete(self):

        # Mark task as not completed
        self._completed = False

    def to_dict(self) -> dict:

        # Convert object data into dictionary format
        # Useful for saving data into JSON/file
        return {
            "task_id": self._task_id,
            "title": self._title,
            "completed": self._completed,
            "created_at": self._created_at,
            "type": "base"
        }

    def __str__(self):

        # User-friendly string representation
        status = "✓" if self._completed else "○"
        return f"[{status}] #{self._task_id} - {self._title}"

    def __repr__(self):

        # Developer-friendly object representation
        return f"BaseTask(id={self._task_id}, title='{self._title}')"