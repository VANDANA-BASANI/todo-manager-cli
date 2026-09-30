"""
storage.py — File Persistence Layer
Handles reading/writing tasks to a JSON file.
"""

import json
import os
from typing import List

from models import Task, task_from_dict


class Storage:
    """Handles file-based persistence using JSON."""

    def __init__(self, filepath: str = "tasks.json"):
        self.filepath = filepath

    def save(self, tasks: List[Task]) -> None:
        """Serialize all tasks and write to JSON file."""
        data = {
            "tasks": [t.to_dict() for t in tasks],
            "next_id": Task._id_counter,
        }
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self) -> List[Task]:
        """Read JSON file and return list of Task objects."""
        if not os.path.exists(self.filepath):
            return []

        with open(self.filepath, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("⚠️  Data file is corrupted. Starting fresh.")
                return []

        # Restore the ID counter so new tasks get unique IDs
        Task._id_counter = data.get("next_id", 1)

        tasks = [task_from_dict(t) for t in data.get("tasks", [])]
        return tasks
