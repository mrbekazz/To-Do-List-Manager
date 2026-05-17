import sys
import os
import unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.base_task import BaseTask
from models.priority_task import PriorityTask, DeadlineTask
from storage.task_manager import TaskManager, TaskIterator, task_generator

class TestBaseTask(unittest.TestCase):
    def setUp(self):
        self.task = BaseTask("Buy groceries")

    def test_task_title_is_set_correctly(self):
        self.assertEqual(self.task.title, "Buy groceries")

    def test_task_starts_incomplete(self):
        self.assertFalse(self.task.completed)

    def test_mark_complete_changes_status(self):
        self.task.mark_complete()
        self.assertTrue(self.task.completed)

    def test_mark_incomplete_resets_status(self):
        self.task.mark_complete()
        self.task.mark_incomplete()
        self.assertFalse(self.task.completed)

    def test_invalid_title_raises_value_error(self):
        with self.assertRaises(ValueError):
            BaseTask("")

    def test_task_id_is_positive_int(self):
        self.assertIsInstance(self.task.task_id, int)
        self.assertGreater(self.task.task_id, 0)

    def test_to_dict_returns_dict(self):
        result = self.task.to_dict()
        self.assertIsInstance(result, dict)
        self.assertIn("title", result)
        self.assertIn("completed", result)


class TestPriorityTask(unittest.TestCase):
    def setUp(self):
        self.task = PriorityTask("Study for exam", priority="high", category="school")

    def test_priority_is_stored(self):
        self.assertEqual(self.task.priority, "high")

    def test_category_is_stored(self):
        self.assertEqual(self.task.category, "school")

    def test_invalid_priority_raises_error(self):
        with self.assertRaises(ValueError):
            PriorityTask("Test", priority="extreme")

    def test_change_priority(self):
        self.task.change_priority("critical")
        self.assertEqual(self.task.priority, "critical")

    def test_priority_score_is_correct(self):
        self.assertEqual(self.task.priority_score(), 3)

    def test_critical_has_highest_score(self):
        t = PriorityTask("Urgent task", priority="critical")
        self.assertEqual(t.priority_score(), 4)

    def test_inheritance_from_base(self):
        self.assertIsInstance(self.task, BaseTask)

    def test_to_dict_contains_priority(self):
        d = self.task.to_dict()
        self.assertIn("priority", d)
        self.assertEqual(d["priority"], "high")


class TestDeadlineTask(unittest.TestCase):
    def setUp(self):
        self.task = DeadlineTask("Submit report", "2025-12-31", "critical", "work")

    def test_deadline_is_stored(self):
        self.assertEqual(self.task.deadline, "2025-12-31")

    def test_invalid_deadline_raises_error(self):
        with self.assertRaises(ValueError):
            DeadlineTask("Bad date", "31/12/2025")

    def test_inherits_from_priority_task(self):
        self.assertIsInstance(self.task, PriorityTask)
        self.assertIsInstance(self.task, BaseTask)

    def test_to_dict_has_deadline(self):
        d = self.task.to_dict()
        self.assertIn("deadline", d)


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager(save_file="data/test_save.json")
        self.manager.add_task(BaseTask("Task One"))
        self.manager.add_task(PriorityTask("Task Two", "high", "work"))
        self.manager.add_task(PriorityTask("Task Three", "low", "home"))

    def test_add_task_increases_count(self):
        before = len(self.manager.get_all_tasks())
        self.manager.add_task(BaseTask("New Task"))
        self.assertEqual(len(self.manager.get_all_tasks()), before + 1)

    def test_delete_task_removes_it(self):
        task = BaseTask("Temp Task")
        self.manager.add_task(task)
        result = self.manager.delete_task(task.task_id)
        self.assertTrue(result)
        self.assertIsNone(self.manager.get_task_by_id(task.task_id))

    def test_delete_nonexistent_returns_false(self):
        result = self.manager.delete_task(99999)
        self.assertFalse(result)

    def test_complete_task(self):
        task = BaseTask("Complete me")
        self.manager.add_task(task)
        self.manager.complete_task(task.task_id)
        found = self.manager.get_task_by_id(task.task_id)
        self.assertTrue(found.completed)

    def test_get_incomplete_filters_correctly(self):
        task = BaseTask("Done task")
        self.manager.add_task(task)
        self.manager.complete_task(task.task_id)
        incomplete = self.manager.get_incomplete_tasks()
        ids = [t.task_id for t in incomplete]
        self.assertNotIn(task.task_id, ids)

    def test_get_completed_filters_correctly(self):
        task = BaseTask("Completed one")
        self.manager.add_task(task)
        self.manager.complete_task(task.task_id)
        completed = self.manager.get_completed_tasks()
        self.assertTrue(any(t.task_id == task.task_id for t in completed))

    def test_filter_by_priority(self):
        high_tasks = self.manager.get_by_priority("high")
        self.assertTrue(all(t.priority == "high" for t in high_tasks))

    def test_search_by_keyword(self):
        results = self.manager.search_tasks("Two")
        self.assertTrue(any("Two" in t.title for t in results))

    def test_get_titles_returns_list(self):
        titles = self.manager.get_titles()
        self.assertIsInstance(titles, list)
        self.assertTrue(all(isinstance(t, str) for t in titles))

    def test_get_stats_returns_dict(self):
        stats = self.manager.get_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn("total", stats)

    def test_json_save_and_load(self):
        self.manager.save_to_json("data/test_round_trip.json")
        manager2 = TaskManager(save_file="data/test_round_trip.json")
        loaded = manager2.load_from_json("data/test_round_trip.json")
        self.assertEqual(loaded, len(self.manager.get_all_tasks()))
        os.remove("data/test_round_trip.json")


class TestIteratorAndGenerator(unittest.TestCase):

    def setUp(self):
        self.manager = TaskManager(save_file="data/test_iter.json")
        t1 = PriorityTask("Critical job", "critical")
        t2 = PriorityTask("Low job", "low")
        t3 = BaseTask("Simple job")
        t3.mark_complete()
        self.manager.add_task(t1)
        self.manager.add_task(t2)
        self.manager.add_task(t3)

    def test_iterator_skips_completed(self):
        it = self.manager.get_task_iterator()
        for task in it:
            self.assertFalse(task.completed)

    def test_generator_sorts_by_priority(self):
        sorted_tasks = list(task_generator(self.manager.get_all_tasks()))
        priority_tasks = [t for t in sorted_tasks if isinstance(t, PriorityTask)]
        if len(priority_tasks) >= 2:
            self.assertGreaterEqual(
                priority_tasks[0].priority_score(),
                priority_tasks[1].priority_score()
            )

if __name__ == "__main__":
    unittest.main(verbosity=2)