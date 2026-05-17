import csv
import json
import os
from models.base_task import BaseTask
from models.priority_task import PriorityTask, DeadlineTask
class TaskIterator:
    def __init__(self, tasks: list):
        self._tasks = [t for t in tasks if not t.completed]
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._tasks):
            raise StopIteration
        task = self._tasks[self._index]
        self._index += 1
        return task


def task_generator(tasks: list):
    priority_tasks = [t for t in tasks if isinstance(t, PriorityTask)]
    others = [t for t in tasks if not isinstance(t, PriorityTask)]
    sorted_priority = sorted(priority_tasks, key=lambda t: t.priority_score(), reverse=True)
    for task in sorted_priority:
        yield task
    for task in others:
        yield task


class TaskManager:
    def __init__(self, save_file: str = "data/tasks.json"):
        self._tasks: list = []
        self._categories: set = set()
        self._stats: dict = {"added": 0, "deleted": 0, "completed": 0}
        self._save_file = save_file
        os.makedirs(os.path.dirname(save_file), exist_ok=True)

    def add_task(self, task: BaseTask) -> None:
        self._tasks.append(task)
        self._stats["added"] += 1
        if isinstance(task, PriorityTask):
            self._categories.add(task.category)

    def delete_task(self, task_id: int) -> bool:
        for i, task in enumerate(self._tasks):
            if task.task_id == task_id:
                self._tasks.pop(i)
                self._stats["deleted"] += 1
                return True
        return False

    def get_task_by_id(self, task_id: int):
        for task in self._tasks:
            if task.task_id == task_id:
                return task
        return None

    def complete_task(self, task_id: int) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_complete()
            self._stats["completed"] += 1
            return True
        return False

    def get_all_tasks(self) -> list:
        return self._tasks

    def get_incomplete_tasks(self) -> list:
        return list(filter(lambda t: not t.completed, self._tasks))

    def get_completed_tasks(self) -> list:
        return list(filter(lambda t: t.completed, self._tasks))

    def get_by_priority(self, priority: str) -> list:
        return list(filter(
            lambda t: isinstance(t, PriorityTask) and t.priority == priority.lower(),
            self._tasks
        ))

    def get_by_category(self, category: str) -> list:
        return list(filter(
            lambda t: isinstance(t, PriorityTask) and t.category == category,
            self._tasks
        ))

    def get_titles(self) -> list:
        return list(map(lambda t: t.title, self._tasks))

    def get_task_iterator(self) -> TaskIterator:
        return TaskIterator(self._tasks)

    def get_sorted_by_priority(self) -> list:
        return list(task_generator(self._tasks))

    def search_tasks(self, keyword: str) -> list:

        keyword = keyword.lower()
        return list(filter(lambda t: keyword in t.title.lower(), self._tasks))

    def get_stats(self) -> dict:
        return {
            **self._stats,
            "total": len(self._tasks),
            "incomplete": len(self.get_incomplete_tasks()),
            "categories": list(self._categories)
        }

    def save_to_json(self, filepath: str = None) -> None:
        filepath = filepath or self._save_file
        data = [task.to_dict() for task in self._tasks]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"  ✔ Tasks saved to '{filepath}'.")

    def load_from_json(self, filepath: str = None) -> int:
        filepath = filepath or self._save_file
        if not os.path.exists(filepath):
            return 0
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._tasks.clear()
        loaded = 0
        for item in data:
            try:
                task = self._reconstruct_task(item)
                if task:
                    self._tasks.append(task)
                    loaded += 1
            except (ValueError, KeyError):
                continue
        return loaded

    def _reconstruct_task(self, data: dict):
        from models.base_task import BaseTask
        task_type = data.get("type", "base")

        if task_type == "deadline":
            task = DeadlineTask(data["title"], data["deadline"],
                                data.get("priority", "high"),
                                data.get("category", "deadline"))
        elif task_type == "priority":
            task = PriorityTask(data["title"],
                                data.get("priority", "medium"),
                                data.get("category", "general"))
        else:
            task = BaseTask(data["title"])

        task._task_id = data["task_id"]
        if data.get("completed"):
            task._completed = True

        if data["task_id"] >= BaseTask._id_counter:
            BaseTask._id_counter = data["task_id"] + 1
        return task

    def export_to_csv(self, filepath: str = "data/tasks_export.csv") -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        fieldnames = ["task_id", "title", "type", "priority", "category", "deadline", "completed", "created_at"]
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for task in self._tasks:
                row = task.to_dict()
                writer.writerow(row)
        print(f"  ✔ Tasks exported to '{filepath}'.")