from models.base_task import BaseTask, log_action
VALID_PRIORITIES = {"low", "medium", "high", "critical"}

class PriorityTask(BaseTask):
    def __init__(self, title: str, priority: str = "medium", category: str = "general"):
        super().__init__(title)
        if priority.lower() not in VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of: {VALID_PRIORITIES}")
        self._priority = priority.lower()
        self._category = category.strip()

    @property
    def priority(self):
        return self._priority

    @property
    def category(self):
        return self._category

    @log_action
    def change_priority(self, new_priority: str):
        if new_priority.lower() not in VALID_PRIORITIES:
            raise ValueError(f"Invalid priority: {new_priority}")
        self._priority = new_priority.lower()

    def priority_score(self) -> int:
        scores = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        return scores.get(self._priority, 0)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "priority": self._priority,
            "category": self._category,
            "type": "priority"
        })
        return data

    def __str__(self):
        status = "✓" if self._completed else "○"
        priority_icons = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}
        icon = priority_icons.get(self._priority, "⚪")
        return (f"[{status}] #{self._task_id} {icon} [{self._priority.upper()}] "
                f"{self._title}  (Category: {self._category})")


class DeadlineTask(PriorityTask):
    def __init__(self, title: str, deadline: str, priority: str = "high", category: str = "deadline"):
        super().__init__(title, priority, category)
        if not self._validate_deadline(deadline):
            raise ValueError("Deadline must be in YYYY-MM-DD format.")
        self._deadline = deadline

    @staticmethod
    def _validate_deadline(deadline: str) -> bool:
        import re
        return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', deadline))

    @property
    def deadline(self):
        return self._deadline

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "deadline": self._deadline,
            "type": "deadline"
        })
        return data

    def __str__(self):
        base = super().__str__()
        return f"{base}  ⏰ Due: {self._deadline}"