import os
import sys
import random
def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def format_separator(char: str = "-", width: int = 55) -> str:
    return f"  {char * width}"

def prompt_str(message: str, allow_empty: bool = True) -> str:
    while True:
        value = input(message).strip()
        if value or allow_empty:
            return value
        print("  ✖ Input cannot be empty. Try again.")

def prompt_int(message: str, min_val: int = None, max_val: int = None) -> int:
    while True:
        try:
            value = int(input(message).strip())
            if min_val is not None and value < min_val:
                print(f"  ✖ Enter a value >= {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"  ✖ Enter a value <= {max_val}.")
                continue
            return value
        except ValueError:
            print("  ✖ Please enter a valid number.")

def generate_sample_tasks() -> list:
    samples = [
        "Buy groceries", "Finish homework", "Call doctor",
        "Read Python book", "Fix the bug", "Submit assignment",
        "Exercise for 30 minutes", "Water the plants", "Pay bills",
        "Review pull request"
    ]
    count = random.randint(3, 6)
    return random.sample(samples, count)