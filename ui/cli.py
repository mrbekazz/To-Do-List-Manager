import sys
import math
from utils.helpers import clear_screen, format_separator, prompt_int, prompt_str
from models.priority_task import PriorityTask, DeadlineTask, VALID_PRIORITIES
from models.base_task import BaseTask
from storage.task_manager import TaskManager
class CLI:
    def __init__(self, manager: TaskManager):
        self._manager = manager
        self._running = True

    def run(self) -> None:
        loaded = self._manager.load_from_json()
        if loaded:
            print(f"\n  ✔ Loaded {loaded} task(s) from save file.")
        while self._running:
            self._display_main_menu()
            choice = prompt_int("  Enter choice: ", min_val=0, max_val=9)
            self._handle_choice(choice)

    def _display_main_menu(self) -> None:
        clear_screen()
        stats = self._manager.get_stats()
        print(format_separator("=", 55))
        print("          📋  TO-DO LIST MANAGER  📋")
        print(format_separator("=", 55))
        print(f"  Tasks: {stats['total']} total | "
              f"{stats['incomplete']} pending | "
              f"{stats['completed']} done")
        print(format_separator("-", 55))
        print("  [1] View All Tasks")
        print("  [2] Add Simple Task")
        print("  [3] Add Priority Task")
        print("  [4] Add Deadline Task")
        print("  [5] Complete a Task")
        print("  [6] Delete a Task")
        print("  [7] Filter / Search Tasks")
        print("  [8] Save & Export")
        print("  [9] View Statistics")
        print("  [0] Exit")
        print(format_separator("=", 55))

    def _handle_choice(self, choice: int) -> None:
        handlers = {
            1: self._view_tasks,
            2: self._add_simple_task,
            3: self._add_priority_task,
            4: self._add_deadline_task,
            5: self._complete_task,
            6: self._delete_task,
            7: self._filter_menu,
            8: self._save_export,
            9: self._view_stats,
            0: self._exit
        }
        action = handlers.get(choice)
        if action:
            action()

    def _view_tasks(self, tasks=None, title="ALL TASKS") -> None:
        clear_screen()
        print(format_separator("=", 55))
        print(f"  {title}")
        print(format_separator("=", 55))

        task_list = tasks if tasks is not None else self._manager.get_sorted_by_priority()

        if not task_list:
            print("  (No tasks found.)")
        else:
            for task in task_list:
                print(f"  {task}")

        print(format_separator("-", 55))
        input("\n  Press Enter to return...")

    def _add_simple_task(self) -> None:
        clear_screen()
        print(format_separator("=", 55))
        print("  ADD SIMPLE TASK")
        print(format_separator("-", 55))
        title = prompt_str("  Task title: ")
        try:
            task = BaseTask(title)
            self._manager.add_task(task)
            print(f"\n  ✔ Task added: {task}")
        except ValueError as e:
            print(f"\n  ✖ Error: {e}")
        input("\n  Press Enter to continue...")

    def _add_priority_task(self) -> None:
        clear_screen()
        print(format_separator("=", 55))
        print("  ADD PRIORITY TASK")
        print(format_separator("-", 55))
        print(f"  Priorities: {', '.join(VALID_PRIORITIES)}")

        title = prompt_str("  Task title: ")
        priority = prompt_str("  Priority [medium]: ") or "medium"
        category = prompt_str("  Category [general]: ") or "general"

        try:
            task = PriorityTask(title, priority, category)
            self._manager.add_task(task)
            print(f"\n  ✔ Task added: {task}")
        except ValueError as e:
            print(f"\n  ✖ Error: {e}")
        input("\n  Press Enter to continue...")

    def _add_deadline_task(self) -> None:
        clear_screen()
        print(format_separator("=", 55))
        print("  ADD DEADLINE TASK")
        print(format_separator("-", 55))

        title = prompt_str("  Task title: ")
        deadline = prompt_str("  Deadline (YYYY-MM-DD): ")
        priority = prompt_str("  Priority [high]: ") or "high"
        category = prompt_str("  Category [deadline]: ") or "deadline"

        try:
            task = DeadlineTask(title, deadline, priority, category)
            self._manager.add_task(task)
            print(f"\n  ✔ Task added: {task}")
        except ValueError as e:
            print(f"\n  ✖ Error: {e}")
        input("\n  Press Enter to continue...")

    def _complete_task(self) -> None:
        clear_screen()
        print(format_separator("=", 55))
        print("  COMPLETE TASK")
        print(format_separator("-", 55))

        iterator = self._manager.get_task_iterator()
        pending = list(iterator)
        if not pending:
            print("  No pending tasks!")
        else:
            for task in pending:
                print(f"  {task}")
            task_id = prompt_int("\n  Enter Task ID to complete: ", min_val=1)
            if self._manager.complete_task(task_id):
                print(f"  ✔ Task #{task_id} marked as complete!")
            else:
                print(f"  ✖ Task #{task_id} not found.")

        input("\n  Press Enter to continue...")

    def _delete_task(self) -> None:
        clear_screen()
        print(format_separator("=", 55))
        print("  DELETE TASK")
        print(format_separator("-", 55))

        for task in self._manager.get_all_tasks():
            print(f"  {task}")

        if not self._manager.get_all_tasks():
            print("  No tasks to delete.")
            input("\n  Press Enter to continue...")
            return

        task_id = prompt_int("\n  Enter Task ID to delete: ", min_val=1)
        confirm = input(f"  Confirm delete Task #{task_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            if self._manager.delete_task(task_id):
                print(f"  ✔ Task #{task_id} deleted.")
            else:
                print(f"  ✖ Task #{task_id} not found.")
        else:
            print("  Cancelled.")
        input("\n  Press Enter to continue...")

    def _filter_menu(self) -> None:
        clear_screen()
        print(format_separator("=", 55))
        print("  FILTER / SEARCH TASKS")
        print(format_separator("-", 55))
        print("  [1] Show Incomplete Tasks")
        print("  [2] Show Completed Tasks")
        print("  [3] Filter by Priority")
        print("  [4] Filter by Category")
        print("  [5] Search by Keyword")
        print("  [0] Back")
        print(format_separator("-", 55))

        choice = prompt_int("  Choice: ", min_val=0, max_val=5)

        if choice == 1:
            self._view_tasks(self._manager.get_incomplete_tasks(), "INCOMPLETE TASKS")
        elif choice == 2:
            self._view_tasks(self._manager.get_completed_tasks(), "COMPLETED TASKS")
        elif choice == 3:
            p = prompt_str("  Priority (low/medium/high/critical): ")
            self._view_tasks(self._manager.get_by_priority(p), f"PRIORITY: {p.upper()}")
        elif choice == 4:
            c = prompt_str("  Category name: ")
            self._view_tasks(self._manager.get_by_category(c), f"CATEGORY: {c}")
        elif choice == 5:
            kw = prompt_str("  Keyword: ")
            self._view_tasks(self._manager.search_tasks(kw), f'SEARCH: "{kw}"')

    def _save_export(self) -> None:
        clear_screen()
        print(format_separator("=", 55))
        print("  SAVE & EXPORT")
        print(format_separator("-", 55))
        print("  [1] Save to JSON")
        print("  [2] Export to CSV")
        print("  [3] Both")
        print("  [0] Back")
        choice = prompt_int("  Choice: ", min_val=0, max_val=3)
        if choice in (1, 3):
            self._manager.save_to_json()
        if choice in (2, 3):
            self._manager.export_to_csv()
        if choice != 0:
            input("\n  Press Enter to continue...")

    def _view_stats(self) -> None:
        clear_screen()
        stats = self._manager.get_stats()
        print(format_separator("=", 55))
        print("  📊 STATISTICS")
        print(format_separator("-", 55))
        total = stats['total'] or 1  # avoid division by zero
        completed = stats['completed']
        completion_rate = math.floor((len(self._manager.get_completed_tasks()) / total) * 100)
        print(f"  Total Tasks Added  : {stats['added']}")
        print(f"  Total Tasks Deleted: {stats['deleted']}")
        print(f"  Currently Active   : {stats['total']}")
        print(f"  Completed          : {len(self._manager.get_completed_tasks())}")
        print(f"  Completion Rate    : {completion_rate}%")
        print(f"  Categories Used    : {', '.join(stats['categories']) or 'None'}")
        print(format_separator("-", 55))

        titles = self._manager.get_titles()
        if titles:
            print("  Task Titles:")
            for t in titles:
                print(f"    • {t}")

        input("\n  Press Enter to return...")

    def _exit(self) -> None:
        self._manager.save_to_json()
        print("\n  👋 Tasks saved. Goodbye!\n")
        sys.exit(0)