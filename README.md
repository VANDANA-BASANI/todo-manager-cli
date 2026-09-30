# Todo Manager — CLI OOP Project

A professional command-line **Todo Manager** built with clean Object-Oriented Python.

## Features

- ✅ Add **Basic**, **Priority**, and **Recurring** tasks
- 📅 Optional due dates
- 🔴 Priority levels (low / medium / high) with escalation
- 🔄 Recurring tasks (daily / weekly / monthly) with cycle reset
- 🔍 Search tasks by keyword
- 📊 Progress statistics with visual progress bar
- 💾 Automatic file persistence (JSON) — data survives restarts

## Tech Stack

- **Python 3.8+** — no third-party dependencies
- **JSON** for file storage

## Project Structure

```
todo_manager/
├── main.py      # Entry point — wires all layers
├── models.py    # Data models (Task, PriorityTask, RecurringTask)
├── storage.py   # JSON persistence layer
├── manager.py   # Business logic (TodoManager)
└── cli.py       # CLI menus — fully separated from logic
```

## OOP Design

```
Task (base)
├── PriorityTask  — adds priority level + escalate()
└── RecurringTask — adds recurrence + reset()
```

| Class | Role |
|---|---|
| `Task` | Base model — title, description, due date, complete/uncomplete |
| `PriorityTask` | Inherits Task + priority (low/medium/high) + escalation |
| `RecurringTask` | Inherits Task + recurrence (daily/weekly/monthly) + reset |
| `Storage` | Reads/writes tasks.json |
| `TodoManager` | Business logic — CRUD, search, stats, auto-save |

## How to Run

```bash
python main.py
```

## Usage Guide

| Option | Action |
|---|---|
| 1 → Add Task | Choose Basic / Priority / Recurring |
| 2 → View Tasks | All / Pending / Completed / Search |
| 3 → Task Actions | Complete, Delete, Escalate, Reset |
| 4 → Statistics | Progress bar + counts |
| 0 → Exit | Saves automatically |
