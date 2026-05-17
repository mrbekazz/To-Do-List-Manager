import re
from datetime import datetime

def log_action(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"  [LOG {timestamp}] {func.__name__} called.")
        return result
    return wrapper

class BaseTask:
    _id_counter = 1
    def __init__(self, title: str):
        if not self._validate_title(title):
            raise ValueError("Task title must be a non-empty string (letters/numbers only).")

        self._task_id = BaseTask._id_counter
        BaseTask._id_counter += 1
        self._title = title.strip()
        self._completed = False
        self._created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _validate_title(title: str) -> bool:
        pattern = r'^[\w\s,.!?\-()]{1,100}$'
        return bool(re.match(pattern, title.strip()))

    @property
    def task_id(self):
        return self._task_id

    @property
    def title(self):
        return self._title

    @property
    def completed(self):
        return self._completed

    @property
    def created_at(self):
        return self._created_at

    @log_action
    def mark_complete(self):
        self._completed = True

    @log_action
    def mark_incomplete(self):
        self._completed = False

    def to_dict(self) -> dict:
        return {
            "task_id": self._task_id,
            "title": self._title,
            "completed": self._completed,
            "created_at": self._created_at,
            "type": "base"
        }

    def __str__(self):
        status = "✓" if self._completed else "○"
        return f"[{status}] #{self._task_id} - {self._title}"

    def __repr__(self):
        return f"BaseTask(id={self._task_id}, title='{self._title}')"