"""
main.py — Entry Point
Wires Storage → TodoManager → CLI together.
"""

import sys
import io

# Fix Windows emoji/unicode encoding FIRST, before any other imports
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")



from storage import Storage
from manager import TodoManager
from cli import main_menu


def main() -> None:
    storage = Storage("tasks.json")   # data lives in tasks.json
    manager = TodoManager(storage)    # manager loads existing data
    main_menu(manager)                # hand control to CLI


if __name__ == "__main__":
    main()
