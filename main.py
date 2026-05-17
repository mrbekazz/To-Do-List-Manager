import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from storage.task_manager import TaskManager
from ui.cli import CLI

def main():
    manager = TaskManager(save_file="data/tasks.json")
    app = CLI(manager)
    app.run()

if __name__ == "__main__":
    main()