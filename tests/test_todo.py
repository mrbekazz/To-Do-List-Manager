# System and operating system modules
import sys
import os

# Python built-in testing framework
import unittest


# Add project root directory into Python path
# Allows importing modules from parent folders
sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), '..')
)

# Import project classes
from models.base_task import BaseTask
from models.priority_task import (
    PriorityTask,
    DeadlineTask
)

from storage.task_manager import (
    TaskManager,
    TaskIterator,
    task_generator
)


# Test cases for BaseTask class
class TestBaseTask(unittest.TestCase):

    def setUp(self):

        # Create fresh task before every test
        self.task = BaseTask("Buy groceries")

    def test_task_title_is_set_correctly(self):

        # Check if title is stored correctly
        self.assertEqual(
            self.task.title,
            "Buy groceries"
        )

    def test_task_starts_incomplete(self):

        # New tasks should start as incomplete
        self.assertFalse(self.task.completed)

    def test_mark_complete_changes_status(self):

        # Mark task as completed
        self.task.mark_complete()

        self.assertTrue(self.task.completed)

    def test_mark_incomplete_resets_status(self):

        # Complete task first
        self.task.mark_complete()

        # Reset completion state
        self.task.mark_incomplete()

        self.assertFalse(self.task.completed)

    def test_invalid_title_raises_value_error(self):

        # Empty title should raise exception
        with self.assertRaises(ValueError):
            BaseTask("")

    def test_task_id_is_positive_int(self):

        # Task ID must be positive integer
        self.assertIsInstance(
            self.task.task_id,
            int
        )

        self.assertGreater(
            self.task.task_id,
            0
        )

    def test_to_dict_returns_dict(self):

        # Convert task into dictionary
        result = self.task.to_dict()

        self.assertIsInstance(result, dict)

        self.assertIn("title", result)
        self.assertIn("completed", result)


# Test cases for PriorityTask class
class TestPriorityTask(unittest.TestCase):

    def setUp(self):

        # Create sample priority task
        self.task = PriorityTask(
            "Study for exam",
            priority="high",
            category="school"
        )

    def test_priority_is_stored(self):

        # Check priority value
        self.assertEqual(
            self.task.priority,
            "high"
        )

    def test_category_is_stored(self):

        # Check category value
        self.assertEqual(
            self.task.category,
            "school"
        )

    def test_invalid_priority_raises_error(self):

        # Invalid priority should raise exception
        with self.assertRaises(ValueError):
            PriorityTask(
                "Test",
                priority="extreme"
            )

    def test_change_priority(self):

        # Change priority dynamically
        self.task.change_priority("critical")

        self.assertEqual(
            self.task.priority,
            "critical"
        )

    def test_priority_score_is_correct(self):

        # "high" priority should return score 3
        self.assertEqual(
            self.task.priority_score(),
            3
        )

    def test_critical_has_highest_score(self):

        # Critical priority should have max score
        t = PriorityTask(
            "Urgent task",
            priority="critical"
        )

        self.assertEqual(
            t.priority_score(),
            4
        )

    def test_inheritance_from_base(self):

        # PriorityTask should inherit BaseTask
        self.assertIsInstance(
            self.task,
            BaseTask
        )

    def test_to_dict_contains_priority(self):

        # Dictionary must include priority
        d = self.task.to_dict()

        self.assertIn("priority", d)

        self.assertEqual(
            d["priority"],
            "high"
        )


# Test cases for DeadlineTask class
class TestDeadlineTask(unittest.TestCase):

    def setUp(self):

        # Create sample deadline task
        self.task = DeadlineTask(
            "Submit report",
            "2025-12-31",
            "critical",
            "work"
        )

    def test_deadline_is_stored(self):

        # Check deadline value
        self.assertEqual(
            self.task.deadline,
            "2025-12-31"
        )

    def test_invalid_deadline_raises_error(self):

        # Invalid date format should raise exception
        with self.assertRaises(ValueError):
            DeadlineTask(
                "Bad date",
                "31/12/2025"
            )

    def test_inherits_from_priority_task(self):

        # DeadlineTask should inherit both
        # PriorityTask and BaseTask
        self.assertIsInstance(
            self.task,
            PriorityTask
        )

        self.assertIsInstance(
            self.task,
            BaseTask
        )

    def test_to_dict_has_deadline(self):

        # Dictionary must contain deadline field
        d = self.task.to_dict()

        self.assertIn("deadline", d)


# Test cases for TaskManager class
class TestTaskManager(unittest.TestCase):

    def setUp(self):

        # Create manager object
        self.manager = TaskManager(
            save_file="data/test_save.json"
        )

        # Add sample tasks
        self.manager.add_task(
            BaseTask("Task One")
        )

        self.manager.add_task(
            PriorityTask(
                "Task Two",
                "high",
                "work"
            )
        )

        self.manager.add_task(
            PriorityTask(
                "Task Three",
                "low",
                "home"
            )
        )

    def test_add_task_increases_count(self):

        # Store current task count
        before = len(
            self.manager.get_all_tasks()
        )

        # Add new task
        self.manager.add_task(
            BaseTask("New Task")
        )

        # Count should increase by 1
        self.assertEqual(
            len(self.manager.get_all_tasks()),
            before + 1
        )

    def test_delete_task_removes_it(self):

        # Create temporary task
        task = BaseTask("Temp Task")

        self.manager.add_task(task)

        # Delete task
        result = self.manager.delete_task(
            task.task_id
        )

        self.assertTrue(result)

        # Task should no longer exist
        self.assertIsNone(
            self.manager.get_task_by_id(
                task.task_id
            )
        )

    def test_delete_nonexistent_returns_false(self):

        # Deleting invalid ID should return False
        result = self.manager.delete_task(99999)

        self.assertFalse(result)

    def test_complete_task(self):

        # Add task and complete it
        task = BaseTask("Complete me")

        self.manager.add_task(task)

        self.manager.complete_task(
            task.task_id
        )

        found = self.manager.get_task_by_id(
            task.task_id
        )

        self.assertTrue(found.completed)

    def test_get_incomplete_filters_correctly(self):

        # Create completed task
        task = BaseTask("Done task")

        self.manager.add_task(task)

        self.manager.complete_task(
            task.task_id
        )

        # Get unfinished tasks
        incomplete = (
            self.manager.get_incomplete_tasks()
        )

        ids = [t.task_id for t in incomplete]

        # Completed task should not appear
        self.assertNotIn(task.task_id, ids)

    def test_get_completed_filters_correctly(self):

        # Create completed task
        task = BaseTask("Completed one")

        self.manager.add_task(task)

        self.manager.complete_task(
            task.task_id
        )

        completed = (
            self.manager.get_completed_tasks()
        )

        self.assertTrue(
            any(
                t.task_id == task.task_id
                for t in completed
            )
        )

    def test_filter_by_priority(self):

        # Filter tasks by priority
        high_tasks = (
            self.manager.get_by_priority("high")
        )

        self.assertTrue(
            all(
                t.priority == "high"
                for t in high_tasks
            )
        )

    def test_search_by_keyword(self):

        # Search task by keyword
        results = self.manager.search_tasks("Two")

        self.assertTrue(
            any(
                "Two" in t.title
                for t in results
            )
        )

    def test_get_titles_returns_list(self):

        # Get task titles only
        titles = self.manager.get_titles()

        self.assertIsInstance(titles, list)

        self.assertTrue(
            all(
                isinstance(t, str)
                for t in titles
            )
        )

    def test_get_stats_returns_dict(self):

        # Statistics should return dictionary
        stats = self.manager.get_stats()

        self.assertIsInstance(stats, dict)

        self.assertIn("total", stats)

    def test_json_save_and_load(self):

        # Save tasks into JSON file
        self.manager.save_to_json(
            "data/test_round_trip.json"
        )

        # Load tasks into new manager
        manager2 = TaskManager(
            save_file="data/test_round_trip.json"
        )

        loaded = manager2.load_from_json(
            "data/test_round_trip.json"
        )

        # Loaded task count should match
        self.assertEqual(
            loaded,
            len(self.manager.get_all_tasks())
        )

        # Delete temporary file
        os.remove("data/test_round_trip.json")


# Test cases for iterator and generator
class TestIteratorAndGenerator(unittest.TestCase):

    def setUp(self):

        # Create manager for testing
        self.manager = TaskManager(
            save_file="data/test_iter.json"
        )

        # Create sample tasks
        t1 = PriorityTask(
            "Critical job",
            "critical"
        )

        t2 = PriorityTask(
            "Low job",
            "low"
        )

        t3 = BaseTask("Simple job")

        # Mark one task as completed
        t3.mark_complete()

        # Add tasks into manager
        self.manager.add_task(t1)
        self.manager.add_task(t2)
        self.manager.add_task(t3)

    def test_iterator_skips_completed(self):

        # Iterator should skip completed tasks
        it = self.manager.get_task_iterator()

        for task in it:
            self.assertFalse(task.completed)

    def test_generator_sorts_by_priority(self):

        # Generator should sort tasks by priority
        sorted_tasks = list(
            task_generator(
                self.manager.get_all_tasks()
            )
        )

        priority_tasks = [
            t for t in sorted_tasks
            if isinstance(t, PriorityTask)
        ]

        # Higher priority tasks should appear first
        if len(priority_tasks) >= 2:

            self.assertGreaterEqual(
                priority_tasks[0].priority_score(),
                priority_tasks[1].priority_score()
            )


# Entry point for running tests
if __name__ == "__main__":

    # Run all tests with detailed output
    unittest.main(verbosity=2)