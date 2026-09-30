"""
models.py — Data Models
Defines the Task hierarchy using OOP and inheritance.

Classes:
    Task           → Base class
    PriorityTask   → Inherits Task, adds priority level
    RecurringTask  → Inherits Task, adds recurrence info
"""

import sys
import io
from datetime import datetime

# Ensure emoji/unicode prints correctly on Windows terminals
if hasattr(sys.stdout, "buffer") and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


class Task:
    """Base class representing a simple todo task."""

    # Class-level counter to auto-generate unique IDs
    _id_counter: int = 1

    def __init__(self, title: str, description: str = "", due_date: str = ""):
        self.id: int = Task._id_counter
        Task._id_counter += 1
        self.title: str = title
        self.description: str = description
        self.due_date: str = due_date               # e.g. "2024-12-31"
        self.completed: bool = False
        self.created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.task_type: str = "basic"               # used to identify subclass in JSON

    # ── Actions ──────────────────────────────────────────────

    def complete(self) -> None:
        """Mark the task as done."""
        self.completed = True

    def uncomplete(self) -> None:
        """Mark the task as not done."""
        self.completed = False

    # ── Serialization ─────────────────────────────────────────

    def to_dict(self) -> dict:
        """Serialize to a plain dict for JSON storage."""
        return {
            "id": self.id,
            "task_type": self.task_type,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "completed": self.completed,
            "created_at": self.created_at,
        }

    def _load_base_fields(self, data: dict) -> None:
        """
        Internal helper: populate base Task fields from a dict.
        Called by subclass from_dict() methods so they don't
        duplicate field-assignment code.
        """
        self.id = data["id"]
        self.title = data["title"]
        self.description = data.get("description", "")
        self.due_date = data.get("due_date", "")
        self.completed = data.get("completed", False)
        self.created_at = data.get("created_at", "")
        self.task_type = data.get("task_type", "basic")

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Deserialize a plain Task from a dictionary."""
        obj = object.__new__(cls)          # allocate without calling __init__
        obj._load_base_fields(data)        # populate shared fields
        return obj

    # ── Display ───────────────────────────────────────────────

    def __str__(self) -> str:
        status = "[x]" if self.completed else "[ ]"
        due = f"  Due: {self.due_date}" if self.due_date else ""
        return (
            f"[{self.id}] {status} {self.title}{due}\n"
            f"     Desc: {self.description or 'No description'}"
        )

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title={self.title!r})"


# ─────────────────────────────────────────────────────────────
# Subclass 1 — PriorityTask
# ─────────────────────────────────────────────────────────────

class PriorityTask(Task):
    """
    A task with an explicit priority level.
    Inherits all Task attributes and adds `priority`.
    """

    VALID_PRIORITIES = ("low", "medium", "high")

    def __init__(self, title: str, description: str = "",
                 due_date: str = "", priority: str = "medium"):
        super().__init__(title, description, due_date)   # call parent __init__
        _p = priority.lower()
        self.priority: str = _p if _p in self.VALID_PRIORITIES else "medium"
        self.task_type = "priority"

    # ── Actions ──────────────────────────────────────────────

    def escalate(self) -> None:
        """Bump priority one level up (low → medium → high)."""
        levels = self.VALID_PRIORITIES
        idx = levels.index(self.priority)
        if idx < len(levels) - 1:
            self.priority = levels[idx + 1]
            print(f"  Priority escalated to '{self.priority.upper()}'")
        else:
            print("  Already at highest priority (HIGH).")

    # ── Serialization ─────────────────────────────────────────

    def to_dict(self) -> dict:
        """Extend parent serialization with priority field."""
        data = super().to_dict()            # call parent to_dict()
        data["priority"] = self.priority
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "PriorityTask":
        obj = object.__new__(cls)
        obj._load_base_fields(data)         # reuse parent helper
        obj.priority = data.get("priority", "medium")
        obj.task_type = "priority"
        return obj

    # ── Display ───────────────────────────────────────────────

    def __str__(self) -> str:
        ICONS = {"low": "[LOW]", "medium": "[MED]", "high": "[HIGH]"}
        icon = ICONS.get(self.priority, "[?]")
        status = "[x]" if self.completed else "[ ]"
        due = f"  Due: {self.due_date}" if self.due_date else ""
        return (
            f"[{self.id}] {status} {icon} {self.title}{due}\n"
            f"     Desc: {self.description or 'No description'}"
        )


# ─────────────────────────────────────────────────────────────
# Subclass 2 — RecurringTask
# ─────────────────────────────────────────────────────────────

class RecurringTask(Task):
    """
    A task that repeats on a schedule (daily / weekly / monthly).
    Inherits all Task attributes and adds `recurrence`.
    """

    VALID_RECURRENCES = ("daily", "weekly", "monthly")

    def __init__(self, title: str, description: str = "",
                 due_date: str = "", recurrence: str = "weekly"):
        super().__init__(title, description, due_date)
        _r = recurrence.lower()
        self.recurrence: str = _r if _r in self.VALID_RECURRENCES else "weekly"
        self.task_type = "recurring"

    # ── Actions ──────────────────────────────────────────────

    def reset(self) -> None:
        """Reset completion status for the next recurrence cycle."""
        self.completed = False
        print(f"  Task reset for next {self.recurrence} cycle.")

    # ── Serialization ─────────────────────────────────────────

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["recurrence"] = self.recurrence
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "RecurringTask":
        obj = object.__new__(cls)
        obj._load_base_fields(data)         # reuse parent helper
        obj.recurrence = data.get("recurrence", "weekly")
        obj.task_type = "recurring"
        return obj

    # ── Display ───────────────────────────────────────────────

    def __str__(self) -> str:
        status = "[x]" if self.completed else "[ ]"
        due = f"  Due: {self.due_date}" if self.due_date else ""
        return (
            f"[{self.id}] {status} [RECURRING:{self.recurrence.upper()}] {self.title}{due}\n"
            f"     Desc: {self.description or 'No description'}"
        )


# ─────────────────────────────────────────────────────────────
# Factory — reconstruct correct subclass from saved JSON
# ─────────────────────────────────────────────────────────────

def task_from_dict(data: dict) -> Task:
    """Return the correct Task subclass based on the task_type field."""
    task_type = data.get("task_type", "basic")
    if task_type == "priority":
        return PriorityTask.from_dict(data)
    elif task_type == "recurring":
        return RecurringTask.from_dict(data)
    else:
        return Task.from_dict(data)
