# Modules for working with CSV, JSON and file system
import csv
import json
import os

# Import task classes
from models.base_task import BaseTask
from models.priority_task import PriorityTask, DeadlineTask


# Custom iterator for iterating through incomplete tasks
class TaskIterator:

    def __init__(self, tasks: list):

        # Store only incomplete tasks
        self._tasks = [t for t in tasks if not t.completed]

        # Current iterator position
        self._index = 0

    def __iter__(self):

        # Return iterator object itself
        return self

    def __next__(self):

        # Stop iteration if all tasks are processed
        if self._index >= len(self._tasks):
            raise StopIteration

        # Get current task
        task = self._tasks[self._index]

        # Move to next index
        self._index += 1

        return task


# Generator function for sorting tasks by priority
def task_generator(tasks: list):

    # Separate priority tasks from normal tasks
    priority_tasks = [
        t for t in tasks if isinstance(t, PriorityTask)
    ]

    others = [
        t for t in tasks if not isinstance(t, PriorityTask)
    ]

    # Sort priority tasks from highest to lowest
    sorted_priority = sorted(
        priority_tasks,
        key=lambda t: t.priority_score(),
        reverse=True
    )

    # Yield sorted priority tasks
    for task in sorted_priority:
        yield task

    # Yield remaining tasks
    for task in others:
        yield task


# Main class responsible for task management
class TaskManager:

    def __init__(
        self,
        save_file: str = "data/tasks.json"
    ):

        # List for storing task objects
        self._tasks: list = []

        # Store unique categories
        self._categories: set = set()

        # Statistics dictionary
        self._stats: dict = {
            "added": 0,
            "deleted": 0,
            "completed": 0
        }

        # Default save file path
        self._save_file = save_file

        # Create folder automatically if it does not exist
        os.makedirs(
            os.path.dirname(save_file),
            exist_ok=True
        )

    def add_task(self, task: BaseTask) -> None:

        # Add task into task list
        self._tasks.append(task)

        # Increase added counter
        self._stats["added"] += 1

        # Save category if task has priority/category
        if isinstance(task, PriorityTask):
            self._categories.add(task.category)

    def delete_task(self, task_id: int) -> bool:

        # Search task by ID
        for i, task in enumerate(self._tasks):

            if task.task_id == task_id:

                # Remove task from list
                self._tasks.pop(i)

                # Increase deleted counter
                self._stats["deleted"] += 1

                return True

        return False

    def get_task_by_id(self, task_id: int):

        # Find task with matching ID
        for task in self._tasks:

            if task.task_id == task_id:
                return task

        return None

    def complete_task(self, task_id: int) -> bool:

        # Find task by ID
        task = self.get_task_by_id(task_id)

        if task:

            # Mark task as completed
            task.mark_complete()

            # Update statistics
            self._stats["completed"] += 1

            return True

        return False

    def get_all_tasks(self) -> list:

        # Return all tasks
        return self._tasks

    def get_incomplete_tasks(self) -> list:

        # Return only unfinished tasks
        return list(
            filter(
                lambda t: not t.completed,
                self._tasks
            )
        )

    def get_completed_tasks(self) -> list:

        # Return only completed tasks
        return list(
            filter(
                lambda t: t.completed,
                self._tasks
            )
        )

    def get_by_priority(self, priority: str) -> list:

        # Filter tasks by priority level
        return list(
            filter(
                lambda t:
                isinstance(t, PriorityTask)
                and t.priority == priority.lower(),
                self._tasks
            )
        )

    def get_by_category(self, category: str) -> list:

        # Filter tasks by category
        return list(
            filter(
                lambda t:
                isinstance(t, PriorityTask)
                and t.category == category,
                self._tasks
            )
        )

    def get_titles(self) -> list:

        # Return list of task titles only
        return list(
            map(
                lambda t: t.title,
                self._tasks
            )
        )

    def get_task_iterator(self) -> TaskIterator:

        # Return custom iterator object
        return TaskIterator(self._tasks)

    def get_sorted_by_priority(self) -> list:

        # Return tasks sorted by priority
        return list(task_generator(self._tasks))

    def search_tasks(self, keyword: str) -> list:

        # Convert keyword to lowercase
        keyword = keyword.lower()

        # Search keyword inside task titles
        return list(
            filter(
                lambda t:
                keyword in t.title.lower(),
                self._tasks
            )
        )

    def get_stats(self) -> dict:

        # Return application statistics
        return {
            **self._stats,
            "total": len(self._tasks),
            "incomplete": len(
                self.get_incomplete_tasks()
            ),
            "categories": list(self._categories)
        }

    def save_to_json(self, filepath: str = None) -> None:

        # Use default save path if filepath is not provided
        filepath = filepath or self._save_file

        # Convert all tasks into dictionaries
        data = [
            task.to_dict()
            for task in self._tasks
        ]

        # Save data into JSON file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(f"  ✔ Tasks saved to '{filepath}'.")

    def load_from_json(self, filepath: str = None) -> int:

        # Use default save path
        filepath = filepath or self._save_file

        # Return 0 if file does not exist
        if not os.path.exists(filepath):
            return 0

        # Load JSON data
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Clear existing tasks
        self._tasks.clear()

        loaded = 0

        # Reconstruct task objects from JSON data
        for item in data:

            try:
                task = self._reconstruct_task(item)

                if task:
                    self._tasks.append(task)
                    loaded += 1

            except (ValueError, KeyError):

                # Skip invalid task data
                continue

        return loaded

    def _reconstruct_task(self, data: dict):

        # Import BaseTask locally
        from models.base_task import BaseTask

        # Get task type
        task_type = data.get("type", "base")

        # Recreate correct task object type
        if task_type == "deadline":

            task = DeadlineTask(
                data["title"],
                data["deadline"],
                data.get("priority", "high"),
                data.get("category", "deadline")
            )

        elif task_type == "priority":

            task = PriorityTask(
                data["title"],
                data.get("priority", "medium"),
                data.get("category", "general")
            )

        else:
            task = BaseTask(data["title"])

        # Restore original task ID
        task._task_id = data["task_id"]

        # Restore completion state
        if data.get("completed"):
            task._completed = True

        # Update global ID counter
        if data["task_id"] >= BaseTask._id_counter:
            BaseTask._id_counter = (
                data["task_id"] + 1
            )

        return task

    def export_to_csv(
        self,
        filepath: str = "data/tasks_export.csv"
    ) -> None:

        # Create export folder if needed
        os.makedirs(
            os.path.dirname(filepath),
            exist_ok=True
        )

        # CSV column names
        fieldnames = [
            "task_id",
            "title",
            "type",
            "priority",
            "category",
            "deadline",
            "completed",
            "created_at"
        ]

        # Export task data into CSV file
        with open(
            filepath,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.DictWriter(
                f,
                fieldnames=fieldnames,
                extrasaction="ignore"
            )

            writer.writeheader()

            for task in self._tasks:

                row = task.to_dict()

                writer.writerow(row)

        print(f"  ✔ Tasks exported to '{filepath}'.")