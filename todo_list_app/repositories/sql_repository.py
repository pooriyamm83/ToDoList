from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.project import Project
from ..models.task import Task, Status as TaskStatus
from ..config import MAX_NUMBER_OF_PROJECT, MAX_NUMBER_OF_TASK

class SQLToDoListRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_project(self, name: str, description: str = "") -> Project:
        if self.db.query(func.count(Project.id)) >= MAX_NUMBER_OF_PROJECT:
            raise ValueError(f"atmost {MAX_NUMBER_OF_PROJECT}projects")
        if self.db.query(Project).filter(Project.name == name).first():
            raise ValueError("duplicate name")
        project = Project(name=name, description=description)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_project(self, project_id: int) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()

    def update_project(self, project_id: int, name: Optional[str] = None, description: Optional[str] = None) -> bool:
        project = self.get_project(project_id)
        if not project:
            return False
        if name:
            if self.db.query(Project).filter(Project.name == name, Project.id != project_id).first():
                raise ValueError("duplicate new name")
            project.name = name
        if description:
            project.description = description
        self.db.commit()
        return True

    def delete_project(self, project_id: int) -> bool:
        project = self.get_project(project_id)
        if not project:
            return False
        self.db.delete(project)
        self.db.commit()
        return True

    def list_projects(self) -> List[Project]:
        return self.db.query(Project).order_by(Project.created_at).all()

    def add_task(self, project_id: int, title: str, description: str = "", due_date: Optional[str] = None) -> Task:
        project = self.get_project(project_id)
        if not project:
            raise ValueError("didn't found project")
        if self.db.query(Task).filter(Task.project_id == project_id).count() >= MAX_NUMBER_OF_TASK:
            raise ValueError(f"atmost {MAX_NUMBER_OF_TASK}tasks")
        task = Task(title=title, description=description, due_date=due_date, project_id=project_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        return self.db.query(Task).filter(Task.project_id == project_id).all()

    def update_task_status(self, task_id: int, new_status: str):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError("task was not found")
        task.status = TaskStatus(new_status)
        self.db.commit()

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, due_date: Optional[str] = None) -> bool:
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
        if title:
            task.title = title
        if description:
            task.description = description
        if due_date:
            task.due_date = due_date
        self.db.commit()
        return True

    def delete_task(self, task_id: int) -> bool:
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
        self.db.delete(task)
        self.db.commit()
        return True

    def get_all_tasks(self) -> List[Task]:
        return self.db.query(Task).all()