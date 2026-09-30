"""test_runner.py — Quick automated test for all modules."""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from storage import Storage
from manager import TodoManager
from models import PriorityTask, RecurringTask, Task

# ── Setup ─────────────────────────────────────────────────────
# Clean up any leftover data from previous runs
if os.path.exists("test_tasks.json"):
    os.remove("test_tasks.json")
# Reset the class-level ID counter for a clean test
Task._id_counter = 1

s = Storage("test_tasks.json")
m = TodoManager(s)

# ── Add all 3 task types ──────────────────────────────────────
t1 = m.add_basic("Buy groceries", "Milk, bread, eggs", "2024-12-01")
t2 = m.add_priority("Fix critical bug", "Null pointer in login", "2024-11-30", "medium")
t3 = m.add_recurring("Daily standup", "Team sync", recurrence="daily")

print("Added 3 tasks.")

# ── Actions ───────────────────────────────────────────────────
m.complete(t1.id)
print("Completed task 1.")

m.escalate_priority(t2.id)  # medium -> high
print("Escalated task 2 priority.")

m.reset_recurring(t3.id)
print("Reset task 3 recurring.")

# ── Display ───────────────────────────────────────────────────
print("\n=== All Tasks ===")
for t in m.all_tasks():
    print(str(t))
    print()

# ── Stats ─────────────────────────────────────────────────────
stats = m.stats()
print("=== Stats ===")
print(stats)
assert stats["total"] == 3, f"Expected 3 total, got {stats['total']}"
assert stats["completed"] == 1
assert stats["pending"] == 2
print("Stats OK.")

# ── Search ────────────────────────────────────────────────────
results = m.search("bug")
assert len(results) == 1
print("Search OK: found", len(results), "result(s) for 'bug'")

# ── Persistence ───────────────────────────────────────────────
s2 = Storage("test_tasks.json")
m2 = TodoManager(s2)
assert len(m2.all_tasks()) == 3, "Expected 3 tasks after reload"
print("Reloaded", len(m2.all_tasks()), "tasks from disk.")

# ── Subclass types survive reload ─────────────────────────────
types_found = {type(t).__name__ for t in m2.all_tasks()}
print("Types after reload:", types_found)
assert "Task" in types_found
assert "PriorityTask" in types_found
assert "RecurringTask" in types_found
print("Subclass types preserved. OK.")

# ── Priority escalation persisted ────────────────────────────
for t in m2.all_tasks():
    if isinstance(t, PriorityTask):
        assert t.priority == "high", f"Expected high, got {t.priority}"
        print("Priority escalation persisted. OK.")

# ── Cleanup ───────────────────────────────────────────────────
os.remove("test_tasks.json")

print("\n=================================================")
print("  ALL TESTS PASSED!")
print("=================================================")
