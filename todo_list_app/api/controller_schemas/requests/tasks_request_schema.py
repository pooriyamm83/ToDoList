from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from todo_list_app.models.task import Status

class TaskCreateRequest(BaseModel):
    project_id: int
    title: str = Field(max_length=30)
    description: Optional[str] = Field(default="", max_length=150)
    status: Optional[str] = Field(default="todo")
    due_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, max_length=30)
    description: Optional[str] = Field(None, max_length=150)
    status: Optional[str] = None
    due_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")