# 📋 To-Do List Manager

> **Course:** Introduction to Programming 2 (Python)  
> **Project:** Final Group Project  
> **Topic:** To-Do List Manager — Add, delete, prioritize, and save tasks

---

## 📌 Overview

A fully-featured command-line application built in Python that lets users manage their daily tasks. Tasks can be created with priority levels and deadlines, marked complete, deleted, filtered, searched, and saved automatically to disk.

The project follows a **modular package architecture** and demonstrates every core concept from the course: OOP, functional programming, file I/O, iterators, decorators, regex, and unit testing.

---

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/mrbekazz/To-Do-List-Manager.git
cd todo-list-manager

# 2. Run the application (no external packages needed)
python main.py

# 3. Run all unit tests
python -m unittest tests/test_todo.py -v
```

> Python 3.8+ required. All dependencies are from the standard library — nothing to install.

---

## 🗂️ Project Structure

```
todo_manager/
│
├── main.py                   # Entry point — imports and orchestrates all modules
├── requirements.txt          # No external dependencies (stdlib only)
├── README.md
│
├── models/                   # OOP layer — task class hierarchy
│   ├── __init__.py
│   ├── base_task.py          # BaseTask + @log_action decorator
│   └── priority_task.py      # PriorityTask, DeadlineTask (inheritance)
│
├── storage/                  # Business logic + persistence
│   ├── __init__.py
│   └── task_manager.py       # TaskManager, TaskIterator, task_generator
│
├── ui/                       # User interface
│   ├── __init__.py
│   └── cli.py                # Full CLI menu system
│
├── utils/                    # Shared helpers
│   ├── __init__.py
│   └── helpers.py            # prompt_int, prompt_str, format_separator
│
├── tests/                    # Unit tests
│   ├── __init__.py
│   └── test_todo.py          # 32 tests using unittest
│
└── data/                     # Auto-created at runtime
    ├── tasks.json            # Primary save file
    └── tasks_export.csv      # CSV export
```

---

## ✨ Features

| Feature | Description |
|---|---|
| Add tasks | Simple, priority (low/medium/high/critical), or deadline tasks |
| Delete tasks | Remove by ID with confirmation prompt |
| Complete tasks | Mark done; iterates only over pending tasks |
| Filter & search | By priority, category, keyword, or completion status |
| Auto-save | Tasks saved to JSON on every exit |
| CSV export | Export full task list for spreadsheet use |
| Sorted view | Tasks displayed by priority score (critical first) |
| Statistics | Completion rate, category list, total counts |

---

## 🏗️ Architecture & Class Hierarchy

```
BaseTask
│   ├── _task_id, _title, _completed, _created_at
│   ├── mark_complete(), mark_incomplete()
│   └── to_dict(), __str__()
│
└── PriorityTask  (extends BaseTask)
    │   ├── _priority, _category
    │   ├── change_priority(), priority_score()
    │   └── to_dict(), __str__()          ← polymorphism
    │
    └── DeadlineTask  (extends PriorityTask)
            ├── _deadline
            └── to_dict(), __str__()      ← polymorphism

TaskManager  ──────────────────────────────  Association
    ├── _tasks      : list
    ├── _categories : set
    ├── _stats      : dict
    ├── CRUD        : add_task(), delete_task(), complete_task()
    ├── Filters     : get_incomplete_tasks(), get_by_priority(), search_tasks()
    ├── Functional  : map → get_titles(), filter → get_incomplete_tasks()
    ├── Iterator    : get_task_iterator() → TaskIterator
    ├── Generator   : task_generator()
    └── File I/O    : save_to_json(), load_from_json(), export_to_csv()

CLI  ──────────────────────────────────────  Association: uses TaskManager
    └── run() → while loop → dict-based menu dispatch
```

---

## 🔧 Logic Flow

```
main.py
  └─▶ TaskManager  (loads saved JSON on startup)
  └─▶ CLI.run()
        └─▶ while loop — display menu
              └─▶ handle_choice(int)
                    ├─▶ View tasks       — sorted by task_generator()
                    ├─▶ Add task         — BaseTask / PriorityTask / DeadlineTask
                    ├─▶ Complete task    — TaskIterator (pending only)
                    ├─▶ Delete task      — by ID with confirmation
                    ├─▶ Filter / Search  — lambda + filter
                    ├─▶ Save / Export    — JSON + CSV
                    ├─▶ Statistics       — math.floor, map
                    └─▶ Exit            — auto-save, sys.exit()
```

---

## 📚 Course Requirements Coverage

| Requirement | Points | Implementation |
|---|---|---|
| Control flow, loops, menus | 10 | `cli.py` — while loop, dict dispatch, conditionals |
| Collections (list, set, dict, tuple) | 8 | `task_manager.py` — `_tasks`, `_categories`, `_stats` |
| File I/O — JSON & CSV | 8 | `save_to_json()`, `load_from_json()`, `export_to_csv()` |
| Core OOP — classes, encapsulation | 15 | `BaseTask` — `_private` attrs, `@property` getters |
| Advanced OOP — inheritance | 12 | `DeadlineTask → PriorityTask → BaseTask` |
| Advanced OOP — association | 12 | `CLI` uses `TaskManager`; `TaskManager` manages tasks |
| Advanced OOP — polymorphism | 12 | `to_dict()`, `__str__()` overridden in all 3 classes |
| Functions, lambda, map, filter | 8 | `get_titles()`, `get_incomplete_tasks()`, `get_by_priority()` |
| Packages with `__init__.py` | 10 | `models/`, `storage/`, `ui/`, `utils/`, `tests/` |
| Unit tests (32 total) | 8 | `tests/test_todo.py` — `unittest`, assertTrue/assertFalse |
| Custom decorator | 3 | `@log_action` in `base_task.py` |
| Custom iterator | 3 | `TaskIterator` — `__iter__`, `__next__` |
| Generator | 3 | `task_generator()` — `yield`, sorted by priority |
| Regex validation | 2 | `_validate_title()`, `_validate_deadline()` — `re` module |
| stdlib modules | 5 | `math`, `sys`, `os`, `random`, `re`, `csv`, `json`, `datetime` |
| PEP8, docstrings, error handling | 4 | All files — Google-style docstrings, try/except |

---

## 🧪 Tests

32 unit tests across 5 test classes, all passing:

```
TestBaseTask          — 7 tests   (title, completion, ID, serialization)
TestPriorityTask      — 8 tests   (priority, category, score, inheritance)
TestDeadlineTask      — 4 tests   (deadline format, inheritance chain)
TestTaskManager       — 10 tests  (CRUD, filters, search, JSON round-trip)
TestIteratorGenerator — 3 tests   (iterator skips completed, generator sorts)
```

Run with:
```bash
python -m unittest tests/test_todo.py -v
```

---

## 👥 Individual Contributions

| Member | Role | Responsible Modules |
|---|---|---|
| Sherkhan Amangeldi | **Models Lead** | `models/base_task.py`, `models/priority_task.py` |
| Bekzat Abilkhayev | **Storage & Logic Lead** | `storage/task_manager.py`, `tests/test_todo.py` |
| Merlati Adaly | **UI Lead** | `ui/cli.py`, `utils/helpers.py`, `main.py` |

---

## 🎨 OOP Design Decisions

**Encapsulation** — All attributes are `_private`. External code reads them through `@property` and mutates them only through defined methods like `mark_complete()` or `change_priority()`. This prevents invalid state.

**Inheritance** — `DeadlineTask → PriorityTask → BaseTask`. Each subclass calls `super().__init__()` and adds only what it needs. The chain is kept shallow (3 levels max) for readability.

**Polymorphism** — `to_dict()` and `__str__()` are defined in `BaseTask` and overridden in each subclass. `TaskManager` works with any task type uniformly — it never needs to check `isinstance` to display or serialize.

**Association** — `CLI` holds a reference to `TaskManager`. `TaskManager` holds a list of task objects. Neither class owns the other — loose coupling, easy to test independently.

---

## 📄 License

This project was created for academic purposes.
