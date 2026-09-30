"""
manager.py — Business Logic Layer
TodoManager orchestrates tasks and calls Storage after every change.
"""

from typing import List, Optional

from models import Task, PriorityTask, RecurringTask
from storage import Storage


class TodoManager:
    """
    Central manager that owns the task list and drives all operations.
    Calls storage.save() after every mutating operation so data is
    never lost even if the program crashes.
    """

    def __init__(self, storage: Storage):
        self._storage: Storage = storage
        self._tasks: List[Task] = self._storage.load()

    # ── Helpers ──────────────────────────────────────────────

    def _save(self) -> None:
        """Persist current state to disk immediately."""
        self._storage.save(self._tasks)

    def _find(self, task_id: int) -> Optional[Task]:
        """Return task by ID or None if not found."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    # ── CRUD Operations ──────────────────────────────────────

    def add_basic(self, title: str, description: str = "", due_date: str = "") -> Task:
        """Create and store a basic Task."""
        task = Task(title, description, due_date)
        self._tasks.append(task)
        self._save()
        return task

    def add_priority(self, title: str, description: str = "",
                     due_date: str = "", priority: str = "medium") -> PriorityTask:
        """Create and store a PriorityTask."""
        task = PriorityTask(title, description, due_date, priority)
        self._tasks.append(task)
        self._save()
        return task

    def add_recurring(self, title: str, description: str = "",
                      due_date: str = "", recurrence: str = "weekly") -> RecurringTask:
        """Create and store a RecurringTask."""
        task = RecurringTask(title, description, due_date, recurrence)
        self._tasks.append(task)
        self._save()
        return task

    def delete(self, task_id: int) -> bool:
        """Remove a task by ID. Returns True if found and deleted."""
        task = self._find(task_id)
        if task:
            self._tasks.remove(task)
            self._save()
            return True
        return False

    def complete(self, task_id: int) -> bool:
        """Mark a task as completed."""
        task = self._find(task_id)
        if task:
            task.complete()
            self._save()
            return True
        return False

    def uncomplete(self, task_id: int) -> bool:
        """Mark a task as not completed."""
        task = self._find(task_id)
        if task:
            task.uncomplete()
            self._save()
            return True
        return False

    def escalate_priority(self, task_id: int) -> bool:
        """Escalate a PriorityTask's priority. Returns False if wrong type."""
        task = self._find(task_id)
        if isinstance(task, PriorityTask):
            task.escalate()
            self._save()
            return True
        return False

    def reset_recurring(self, task_id: int) -> bool:
        """Reset a RecurringTask for the next cycle."""
        task = self._find(task_id)
        if isinstance(task, RecurringTask):
            task.reset()
            self._save()
            return True
        return False

    # ── Queries ──────────────────────────────────────────────

    def all_tasks(self) -> List[Task]:
        return list(self._tasks)

    def pending_tasks(self) -> List[Task]:
        return [t for t in self._tasks if not t.completed]

    def completed_tasks(self) -> List[Task]:
        return [t for t in self._tasks if t.completed]

    def search(self, keyword: str) -> List[Task]:
        kw = keyword.lower()
        return [
            t for t in self._tasks
            if kw in t.title.lower() or kw in t.description.lower()
        ]

    def stats(self) -> dict:
        total = len(self._tasks)
        done = len(self.completed_tasks())
        return {
            "total": total,
            "completed": done,
            "pending": total - done,
            "percent": round((done / total) * 100, 1) if total else 0,
        }
