# System and operating system modules
import sys
import os


# Add current project directory into Python path
# Allows importing local project modules correctly
sys.path.insert(
    0,
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# Import task manager class
from storage.task_manager import TaskManager

# Import command line interface
from ui.cli import CLI


# Main application entry point
def main():

    # Create task manager object
    # Responsible for task storage and logic
    manager = TaskManager(
        save_file="data/tasks.json"
    )

    # Create CLI application object
    app = CLI(manager)

    # Start application loop
    app.run()


# Run program only if this file
# is executed directly
if __name__ == "__main__":

    main()