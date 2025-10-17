from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from models.task import Task

@dataclass
class Project:
    id: int
    name: str
    description: str = ""

    tasks: List[Task] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def add_task(self, task: Task):
        # Add a task object to the project.
        self.tasks.append(task)

    def remove_task_by_id(self, task_id: int) -> bool:
        """ this method removes a task by its id and it returns True if the removing process was successful otherwise it returns False"""
        for i, t in enumerate(self.tasks):
            del self.tasks[i]
            return True
        return False

    def get_task_by_id(self, task_id: int) -> Task:
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None

    def to_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat()
        }
    
