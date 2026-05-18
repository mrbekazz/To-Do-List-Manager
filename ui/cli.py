# System and mathematical modules
import sys
import math

# Import helper functions for CLI interface
from utils.helpers import (
    clear_screen,
    format_separator,
    prompt_int,
    prompt_str
)

# Import task classes and constants
from models.priority_task import (
    PriorityTask,
    DeadlineTask,
    VALID_PRIORITIES
)

from models.base_task import BaseTask

# Import task manager
from storage.task_manager import TaskManager


# Command Line Interface class
# Handles all user interaction in terminal
class CLI:

    def __init__(self, manager: TaskManager):

        # Store task manager object
        self._manager = manager

        # Application running state
        self._running = True

    def run(self) -> None:

        # Load saved tasks at startup
        loaded = self._manager.load_from_json()

        if loaded:
            print(
                f"\n  ✔ Loaded {loaded} "
                f"task(s) from save file."
            )

        # Main application loop
        while self._running:

            self._display_main_menu()

            # Get user menu choice
            choice = prompt_int(
                "  Enter choice: ",
                min_val=0,
                max_val=9
            )

            # Execute selected action
            self._handle_choice(choice)

    def _display_main_menu(self) -> None:

        # Clear terminal screen
        clear_screen()

        # Get current statistics
        stats = self._manager.get_stats()

        print(format_separator("=", 55))
        print("          📋  TO-DO LIST MANAGER  📋")
        print(format_separator("=", 55))

        # Display short task summary
        print(
            f"  Tasks: {stats['total']} total | "
            f"{stats['incomplete']} pending | "
            f"{stats['completed']} done"
        )

        print(format_separator("-", 55))

        # Main menu options
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

        # Dictionary mapping menu numbers to methods
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

        # Get corresponding method
        action = handlers.get(choice)

        # Execute selected method
        if action:
            action()

    def _view_tasks(
        self,
        tasks=None,
        title="ALL TASKS"
    ) -> None:

        clear_screen()

        print(format_separator("=", 55))
        print(f"  {title}")
        print(format_separator("=", 55))

        # Use provided task list
        # or show all sorted tasks
        task_list = (
            tasks
            if tasks is not None
            else self._manager.get_sorted_by_priority()
        )

        # Check if list is empty
        if not task_list:
            print("  (No tasks found.)")

        else:

            # Print all tasks
            for task in task_list:
                print(f"  {task}")

        print(format_separator("-", 55))

        input("\n  Press Enter to return...")

    def _add_simple_task(self) -> None:

        clear_screen()

        print(format_separator("=", 55))
        print("  ADD SIMPLE TASK")
        print(format_separator("-", 55))

        # Get task title from user
        title = prompt_str("  Task title: ")

        try:

            # Create simple task object
            task = BaseTask(title)

            # Add task into manager
            self._manager.add_task(task)

            print(f"\n  ✔ Task added: {task}")

        except ValueError as e:

            # Handle invalid input
            print(f"\n  ✖ Error: {e}")

        input("\n  Press Enter to continue...")

    def _add_priority_task(self) -> None:

        clear_screen()

        print(format_separator("=", 55))
        print("  ADD PRIORITY TASK")
        print(format_separator("-", 55))

        # Show available priorities
        print(
            f"  Priorities: "
            f"{', '.join(VALID_PRIORITIES)}"
        )

        # Get task information
        title = prompt_str("  Task title: ")

        priority = (
            prompt_str("  Priority [medium]: ")
            or "medium"
        )

        category = (
            prompt_str("  Category [general]: ")
            or "general"
        )

        try:

            # Create priority task
            task = PriorityTask(
                title,
                priority,
                category
            )

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

        # Get deadline task information
        title = prompt_str("  Task title: ")

        deadline = prompt_str(
            "  Deadline (YYYY-MM-DD): "
        )

        priority = (
            prompt_str("  Priority [high]: ")
            or "high"
        )

        category = (
            prompt_str("  Category [deadline]: ")
            or "deadline"
        )

        try:

            # Create deadline task
            task = DeadlineTask(
                title,
                deadline,
                priority,
                category
            )

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

        # Get iterator for incomplete tasks
        iterator = self._manager.get_task_iterator()

        pending = list(iterator)

        # Check if unfinished tasks exist
        if not pending:
            print("  No pending tasks!")

        else:

            # Display pending tasks
            for task in pending:
                print(f"  {task}")

            # Ask for task ID
            task_id = prompt_int(
                "\n  Enter Task ID to complete: ",
                min_val=1
            )

            # Complete selected task
            if self._manager.complete_task(task_id):

                print(
                    f"  ✔ Task #{task_id} "
                    f"marked as complete!"
                )

            else:
                print(
                    f"  ✖ Task #{task_id} not found."
                )

        input("\n  Press Enter to continue...")

    def _delete_task(self) -> None:

        clear_screen()

        print(format_separator("=", 55))
        print("  DELETE TASK")
        print(format_separator("-", 55))

        # Display all tasks
        for task in self._manager.get_all_tasks():
            print(f"  {task}")

        # Check if task list is empty
        if not self._manager.get_all_tasks():

            print("  No tasks to delete.")

            input("\n  Press Enter to continue...")

            return

        # Ask for task ID
        task_id = prompt_int(
            "\n  Enter Task ID to delete: ",
            min_val=1
        )

        # Ask for confirmation
        confirm = input(
            f"  Confirm delete Task "
            f"#{task_id}? (y/n): "
        ).strip().lower()

        if confirm == 'y':

            # Delete selected task
            if self._manager.delete_task(task_id):

                print(
                    f"  ✔ Task #{task_id} deleted."
                )

            else:
                print(
                    f"  ✖ Task #{task_id} not found."
                )

        else:
            print("  Cancelled.")

        input("\n  Press Enter to continue...")

    def _filter_menu(self) -> None:

        clear_screen()

        print(format_separator("=", 55))
        print("  FILTER / SEARCH TASKS")
        print(format_separator("-", 55))

        # Filter menu options
        print("  [1] Show Incomplete Tasks")
        print("  [2] Show Completed Tasks")
        print("  [3] Filter by Priority")
        print("  [4] Filter by Category")
        print("  [5] Search by Keyword")
        print("  [0] Back")

        print(format_separator("-", 55))

        # Get user choice
        choice = prompt_int(
            "  Choice: ",
            min_val=0,
            max_val=5
        )

        # Show incomplete tasks
        if choice == 1:

            self._view_tasks(
                self._manager.get_incomplete_tasks(),
                "INCOMPLETE TASKS"
            )

        # Show completed tasks
        elif choice == 2:

            self._view_tasks(
                self._manager.get_completed_tasks(),
                "COMPLETED TASKS"
            )

        # Filter by priority
        elif choice == 3:

            p = prompt_str(
                "  Priority "
                "(low/medium/high/critical): "
            )

            self._view_tasks(
                self._manager.get_by_priority(p),
                f"PRIORITY: {p.upper()}"
            )

        # Filter by category
        elif choice == 4:

            c = prompt_str("  Category name: ")

            self._view_tasks(
                self._manager.get_by_category(c),
                f"CATEGORY: {c}"
            )

        # Search by keyword
        elif choice == 5:

            kw = prompt_str("  Keyword: ")

            self._view_tasks(
                self._manager.search_tasks(kw),
                f'SEARCH: "{kw}"'
            )

    def _save_export(self) -> None:

        clear_screen()

        print(format_separator("=", 55))
        print("  SAVE & EXPORT")
        print(format_separator("-", 55))

        # Save/export options
        print("  [1] Save to JSON")
        print("  [2] Export to CSV")
        print("  [3] Both")
        print("  [0] Back")

        choice = prompt_int(
            "  Choice: ",
            min_val=0,
            max_val=3
        )

        # Save tasks into JSON
        if choice in (1, 3):
            self._manager.save_to_json()

        # Export tasks into CSV
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

        # Avoid division by zero
        total = stats['total'] or 1

        completed = stats['completed']

        # Calculate completion percentage
        completion_rate = math.floor(
            (
                len(
                    self._manager.get_completed_tasks()
                ) / total
            ) * 100
        )

        # Display statistics
        print(
            f"  Total Tasks Added  : "
            f"{stats['added']}"
        )

        print(
            f"  Total Tasks Deleted: "
            f"{stats['deleted']}"
        )

        print(
            f"  Currently Active   : "
            f"{stats['total']}"
        )

        print(
            f"  Completed          : "
            f"{len(self._manager.get_completed_tasks())}"
        )

        print(
            f"  Completion Rate    : "
            f"{completion_rate}%"
        )

        print(
            f"  Categories Used    : "
            f"{', '.join(stats['categories']) or 'None'}"
        )

        print(format_separator("-", 55))

        # Display all task titles
        titles = self._manager.get_titles()

        if titles:

            print("  Task Titles:")

            for t in titles:
                print(f"    • {t}")

        input("\n  Press Enter to return...")

    def _exit(self) -> None:

        # Automatically save tasks before exit
        self._manager.save_to_json()

        print("\n  👋 Tasks saved. Goodbye!\n")

        # Stop application
        sys.exit(0)