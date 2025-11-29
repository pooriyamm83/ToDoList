from datetime import datetime
from typing import List
from uuid import uuid4
from .task import Task

class Project:
    def __init__(self, name: str, description: str = ""):
        if len(name) > 30:
            raise ValueError("Project name must be at most 30 characters long.")
        if len(description) > 150:
            raise ValueError("Project description must be at most 150 characters long.")
        self.id = str(uuid4())
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        from config import MAX_NUMBER_OF_TASK
        if len(self.tasks) >= MAX_NUMBER_OF_TASK:
            raise ValueError(f"Maximum of {MAX_NUMBER_OF_TASK} tasks per project.")
        self.tasks.append(task)

    def __str__(self):
        return f"[{self.id[:8]}] {self.name} ({len(self.tasks)} tasks)"
