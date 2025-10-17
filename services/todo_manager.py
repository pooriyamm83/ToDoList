import os
from datetime import datetime
from typing import List, Optional
from dotenv import load_dotenv

from models.project import Project
from models.task import Task

load_dotenv()

# limits
MAX_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECTS", "10"))
MAX_TASKS_PER_PROJECT = int(os.getenv("MAX_NUMBER_OF_TASKS", "50"))
VALID_STATUSES = {"todo", "doing", "done"}

class ToDoManager:
    def __init__(self):
        self._projects: List[Project] = []
        self._next_project_id = 1
        # track task id per project by storing next id inside project id mapping
        # we will keep a small dict mapping project.id -> next_task_id
        self._next_task_id = {}

    def list_projects(self) -> List[Project]:
        # this method returns the projects list based on the order of their creation time
        return sorted(self._projects, key=lambda p: p.created_at)

    def create_project(self, name: str, description: str = "") -> Project:
        """Create a new project after validation."""
        name = name.strip()
        if not name:
            raise ValueError("Project name cannot be empty")
        if len(name) > 30:
            raise ValueError("Project name must be at most 30 characters")
        if len(description) > 150:
            raise ValueError("Description must be at most 150 characters")
        if len(self._projects) >= MAX_PROJECTS:
            raise ValueError("Max number of projects reached")
        if any(p.name.lower() == name.lower() for p in self._projects):
            raise ValueError("Project name already exists")

        project = Project(id = self._next_project_id, name=name, description=description)
        self._projects.append(project)
        self._next_task_id[project.id] = 1
        self._next_project_id += 1
        return project

    def get_project(self, project_id: int) -> Optional[Project]:
        for p in self._projects:
            if p.id == project_id:
                return p
        return None

    def edit_project(self, project_id: int, new_name: Optional[str] = None, new_description: Optional[str] = None) -> Project:
        project = self.get_project(project_id)
        if not project:
            raise ValueError("Project not found")
        if new_name is not None:
            new_name = new_name.strip()
            if not new_name:
                raise ValueError("Project name cannot be empty")
            if len(new_name) > 30:
                raise ValueError("Project name must be at most 30 characters")
            if any(p.id != project_id and p.name.lower() == new_name.lower() for p in self._projects):
                raise ValueError("Project name already exists")
            project.name = new_name
        if new_description is not None:
            if len(new_description) > 150:
                raise ValueError("Description must be at most 150 characters")
            project.description = new_description
        return project

    def delete_project(self, project_id: int) -> bool:
        """delete a project if wasn't successful just return False"""
        for i, p in enumerate(self._projects):
            if p.id == project_id:
                del self._projects[i]
                self._next_task_id.pop(project_id)
                return True
        return False

    def _parse_deadline(selfself, deadline_str: Optional[str]) -> Optional[datetime]:
        if not deadline_str:
            return None
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"):
            try:
                return datetime.strptime(deadline_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Deadline {deadline_str} is not valid")

    def add_task(self, project_id: int, title: str, description: str = "", status: str = "todo", deadline: Optional[str] = None) -> Task:
        project = self.get_project(project_id)
        if not project:
            raise ValueError("Project not found")
        if len(project.tasks) >= MAX_TASKS_PER_PROJECT:
            raise ValueError("Max tasks for this project reached")
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty")
        if len(title) > 30:
            raise ValueError("Task title must be at most 30 characters")
        if len(description) > 150:
            raise ValueError("Task description must be at most 150 characters")
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}")
        dl = self._parse_deadline(deadline) if deadline else None
        next_tid = self._next_task_id.get(project_id, 1)
        task = Task(id = next_tid, title = title, description = description, status = status, deadline = dl)
        project.add_task(task)
        self._next_task_id[project_id] = next_tid + 1
        return task

    def edit_task(self, project_id: int, task_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[str] = None, deadline: Optional[str] = None) -> Task:
        project = self.get_project(project_id)
        if not project:
            raise ValueError("Project not found")
        task = project.get_task_by_id(task_id)
        if not task:
            raise ValueError("Task not found")

        if title is not None:
            title = title.strip()
            if not title:
                raise ValueError("Task title cannot be empty")
            if len(title) > 30:
                raise ValueError("Task title must be at most 30 characters")
            task.title = title

        if description is not None:
            if len(description) > 150:
                raise ValueError("Task description must be at most 150 characters")
            task.description = description

        if status is not None:
            if status not in VALID_STATUSES:
                raise ValueError(f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}")
            task.status = status

        if deadline is not None:
            task.deadline = self._parse_deadline(deadline) if deadline else None

        return task

    def delete_task(self, project_id: int, task_id: int) -> bool:
        project = self.get_project(project_id)
        if not project:
            raise ValueError("Project not found")
        return project.remove_task_by_id(task_id)

    def list_tasks(self, project_id: int) -> List[Task]:
        project = self.get_project(project_id)
        if not project:
            raise ValueError("Project not found")
        return project.tasks.copy() # return a copy

