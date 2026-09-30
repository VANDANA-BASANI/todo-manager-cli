"""
cli.py — Command-Line Interface
Renders menus and handles user input. Completely separated from business logic.
"""

import os
import sys
import io

# Ensure unicode works on Windows
if hasattr(sys.stdout, "buffer") and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from manager import TodoManager


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def divider(char: str = "-", width: int = 55) -> None:
    print(char * width)


def header() -> None:
    clear()
    divider("=")
    print("     TODO MANAGER  --  CLI OOP Edition")
    divider("=")


def pause() -> None:
    input("\n  Press Enter to continue...")


def get_input(prompt: str, required: bool = True) -> str:
    while True:
        value = input(f"  {prompt}: ").strip()
        if value or not required:
            return value
        print("  [!] This field is required.")


def print_tasks(tasks: list) -> None:
    if not tasks:
        print("  (no tasks found)")
        return
    divider()
    for task in tasks:
        for line in str(task).splitlines():
            print(f"  {line}")
        print(f"       Created: {task.created_at}  |  Type: {task.task_type}")
        divider(".")
    print()


# ─────────────────────────────────────────────────────────────
# Sub-menus
# ─────────────────────────────────────────────────────────────

def menu_add(manager: TodoManager) -> None:
    header()
    print("  ADD NEW TASK\n")
    print("  [1] Basic Task")
    print("  [2] Priority Task  (low / medium / high urgency)")
    print("  [3] Recurring Task (daily / weekly / monthly)")
    print("  [0] Back")
    divider()
    choice = input("  Choose: ").strip()

    if choice == "0":
        return

    title = get_input("Title")
    desc = get_input("Description (optional)", required=False)
    due = get_input("Due date YYYY-MM-DD (optional)", required=False)

    if choice == "1":
        task = manager.add_basic(title, desc, due)
        print(f"\n  [OK] Basic task #{task.id} '{task.title}' added!")

    elif choice == "2":
        print("\n  Priority options: low | medium | high")
        priority = get_input("Priority (default: medium)", required=False) or "medium"
        task = manager.add_priority(title, desc, due, priority)
        print(f"\n  [OK] Priority task #{task.id} added with priority: {task.priority.upper()}")

    elif choice == "3":
        print("\n  Recurrence options: daily | weekly | monthly")
        recurrence = get_input("Recurrence (default: weekly)", required=False) or "weekly"
        task = manager.add_recurring(title, desc, due, recurrence)
        print(f"\n  [OK] Recurring task #{task.id} added ({task.recurrence})")

    else:
        print("  [!] Invalid option.")

    pause()


def menu_view(manager: TodoManager) -> None:
    header()
    print("  VIEW TASKS\n")
    print("  [1] All Tasks")
    print("  [2] Pending Only")
    print("  [3] Completed Only")
    print("  [4] Search by keyword")
    print("  [0] Back")
    divider()
    choice = input("  Choose: ").strip()

    header()
    if choice == "1":
        print("  ALL TASKS")
        print_tasks(manager.all_tasks())
    elif choice == "2":
        print("  PENDING TASKS")
        print_tasks(manager.pending_tasks())
    elif choice == "3":
        print("  COMPLETED TASKS")
        print_tasks(manager.completed_tasks())
    elif choice == "4":
        kw = get_input("Search keyword")
        results = manager.search(kw)
        print(f"\n  RESULTS FOR '{kw}':")
        print_tasks(results)
    elif choice == "0":
        return
    else:
        print("  [!] Invalid option.")

    pause()


def menu_actions(manager: TodoManager) -> None:
    header()
    print("  TASK ACTIONS\n")
    print("  [1] Mark Complete")
    print("  [2] Mark Incomplete")
    print("  [3] Delete Task")
    print("  [4] Escalate Priority  (Priority tasks only)")
    print("  [5] Reset Recurring    (Recurring tasks only)")
    print("  [0] Back")
    divider()
    choice = input("  Choose: ").strip()

    if choice == "0":
        return

    try:
        task_id = int(get_input("Task ID"))
    except ValueError:
        print("  [!] Invalid ID — must be a number.")
        pause()
        return

    if choice == "1":
        ok = manager.complete(task_id)
        print(f"  {'[OK] Marked complete!' if ok else '[!] Task not found.'}")

    elif choice == "2":
        ok = manager.uncomplete(task_id)
        print(f"  {'[OK] Marked incomplete.' if ok else '[!] Task not found.'}")

    elif choice == "3":
        confirm = input(f"  Delete task #{task_id}? (y/n): ").lower()
        if confirm == "y":
            ok = manager.delete(task_id)
            print(f"  {'[OK] Deleted.' if ok else '[!] Task not found.'}")
        else:
            print("  Cancelled.")

    elif choice == "4":
        ok = manager.escalate_priority(task_id)
        if not ok:
            print("  [!] Not a priority task, or task not found.")

    elif choice == "5":
        ok = manager.reset_recurring(task_id)
        if not ok:
            print("  [!] Not a recurring task, or task not found.")

    else:
        print("  [!] Invalid option.")

    pause()


def menu_stats(manager: TodoManager) -> None:
    header()
    s = manager.stats()
    print("  STATISTICS\n")
    divider()
    print(f"  Total Tasks  : {s['total']}")
    print(f"  Completed    : {s['completed']}")
    print(f"  Pending      : {s['pending']}")
    print(f"  Progress     : {s['percent']}%")
    divider()
    # Simple ASCII progress bar
    filled = int(s["percent"] / 5)
    bar = "#" * filled + "-" * (20 - filled)
    print(f"  [{bar}] {s['percent']}%")
    pause()


# ─────────────────────────────────────────────────────────────
# Main Menu Loop
# ─────────────────────────────────────────────────────────────

def main_menu(manager: TodoManager) -> None:
    while True:
        header()
        pending = len(manager.pending_tasks())
        print(f"  You have {pending} pending task(s)\n")
        print("  [1] Add Task")
        print("  [2] View Tasks")
        print("  [3] Task Actions  (complete / delete / escalate)")
        print("  [4] Statistics")
        print("  [0] Exit")
        divider()
        choice = input("  Choose: ").strip()

        if choice == "1":
            menu_add(manager)
        elif choice == "2":
            menu_view(manager)
        elif choice == "3":
            menu_actions(manager)
        elif choice == "4":
            menu_stats(manager)
        elif choice == "0":
            print("\n  Goodbye! Your tasks have been saved.\n")
            break
        else:
            print("  [!] Invalid option.")
            pause()
