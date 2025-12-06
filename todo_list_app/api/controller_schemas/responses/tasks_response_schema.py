from pydantic import BaseModel, ConfigDict
from datetime import datetime
from todo_list_app.models.task import Status
from typing import List, Optional

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: Status
    due_date: Optional[str]
    created_at: datetime
    project_id: int

    model_config = ConfigDict(from_attributes=True)