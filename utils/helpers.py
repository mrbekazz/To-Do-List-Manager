# Modules for system operations and random generation
import os
import sys
import random


# Clears terminal screen depending on operating system
def clear_screen() -> None:

    # Windows uses 'cls', Linux/macOS uses 'clear'
    os.system(
        'cls'
        if os.name == 'nt'
        else 'clear'
    )


# Creates formatted separator line for CLI interface
def format_separator(
    char: str = "-",
    width: int = 55
) -> str:

    # Repeat selected character multiple times
    return f"  {char * width}"


# Safely gets string input from user
def prompt_str(
    message: str,
    allow_empty: bool = True
) -> str:

    while True:

        # Remove extra spaces from input
        value = input(message).strip()

        # Return value if valid
        if value or allow_empty:
            return value

        # Error message for empty input
        print(
            "  ✖ Input cannot be empty. "
            "Try again."
        )


# Safely gets integer input from user
def prompt_int(
    message: str,
    min_val: int = None,
    max_val: int = None
) -> int:

    while True:

        try:

            # Convert user input into integer
            value = int(
                input(message).strip()
            )

            # Validate minimum allowed value
            if (
                min_val is not None
                and value < min_val
            ):

                print(
                    f"  ✖ Enter a value "
                    f">= {min_val}."
                )

                continue

            # Validate maximum allowed value
            if (
                max_val is not None
                and value > max_val
            ):

                print(
                    f"  ✖ Enter a value "
                    f"<= {max_val}."
                )

                continue

            return value

        except ValueError:

            # Handle invalid numeric input
            print(
                "  ✖ Please enter "
                "a valid number."
            )


# Generates random sample task titles
def generate_sample_tasks() -> list:

    # Predefined sample tasks
    samples = [
        "Buy groceries",
        "Finish homework",
        "Call doctor",
        "Read Python book",
        "Fix the bug",
        "Submit assignment",
        "Exercise for 30 minutes",
        "Water the plants",
        "Pay bills",
        "Review pull request"
    ]

    # Generate random number of tasks
    count = random.randint(3, 6)

    # Return random unique task titles
    return random.sample(samples, count)