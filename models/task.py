from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: str = ""                   # optional
    status: str = "todo"                    # one of todo, doing, done
    deadline: Optional[datetime] = None     # optional datetime

    created_at: datetime = field(default_factory= datetime.utcnow)

    def to_dictionary(self):
        """Return a serializable representation (helpful for printing)."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }