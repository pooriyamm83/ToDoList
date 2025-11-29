from datetime import datetime
from typing import Optional
from uuid import uuid4
from enum import Enum

class Status(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class Task:
    def __init__(self, title: str, description: str = "", status: str = "todo", due_date: Optional[str] = None):
        if len(title) > 30:
            raise ValueError("Task title must be at most 30 characters long.")
        if len(description) > 150:
            raise ValueError("Task description must be at most 150 characters long.")
        if status not in {s.value for s in Status}:
            raise ValueError("Invalid status value.")
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")

        self.id = str(uuid4())
        self.title = title
        self.description = description
        self.status = Status(status)
        self.due_date = due_date
        self.created_at = datetime.now()

    def __str__(self):
        due = f" (Deadline: {self.due_date})" if self.due_date else ""
        return f"{self.status.value.upper()} [{self.id[:8]}] {self.title}{due}"
