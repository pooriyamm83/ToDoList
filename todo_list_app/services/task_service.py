from todo_list_app.models.task import Task, Status
from typing import List, Optional
from sqlalchemy.orm import Session
from todo_list_app.repositories.task_repository import TaskRepository
from todo_list_app.exceptions.service_exceptions import ValidationError
from datetime import datetime

class TaskService:
    def __init__(self, db: Session):
        self.repo = TaskRepository(db)

    def create_task(self, project_id: int, title: str, description: str = "", status: Status = Status.TODO, due_date: Optional[str] = None) -> Task:
        if len(title) > 30:
            raise ValidationError("task title 30 char maximum")
        if len(description) > 150:
            raise ValidationError("explanation 150 char maximum")
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                raise ValidationError("deadlines format should look like YYYY-MM-DD")
        return self.repo.create(project_id, title, description, status, due_date)

    def list_tasks(self, project_id: int) -> List[Task]:
        return self.repo.get_by_project(project_id)

    def update_task_status(self, task_id: int, new_status: Status) -> Task:
        return self.repo.update(task_id, status=new_status)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, due_date: Optional[str] = None) -> Task:
        if title and len(title) > 30:
            raise ValidationError("new title 30 char maximum")
        if description and len(description) > 150:
            raise ValidationError("new explanation 150 char maximum")
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                raise ValidationError("deadlines format should look like YYYY-MM-DD")
        return self.repo.update(task_id, title, description, due_date=due_date)

    def delete_task(self, task_id: int) -> None:
        self.repo.delete(task_id)