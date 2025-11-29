from typing import Dict, List, Optional
from .models.project import Project
from .models.task import Task
from .config import MAX_NUMBER_OF_PROJECT


class ToDoListRepository:
    def __init__(self):
        self.projects: Dict[str, Project] = {}

    def create_project(self, name: str, description: str = "") -> Project:
        if len(self.projects) >= MAX_NUMBER_OF_PROJECT:
            raise ValueError(f"A maximum of {MAX_NUMBER_OF_PROJECT} projects is allowed.")
        if any(p.name == name for p in self.projects.values()):
            raise ValueError("Project name must be unique.")

        project = Project(name, description)
        self.projects[project.id] = project
        return project

    def update_project(self, project_id: str, name: str = None, description: str = None) -> bool:
        project = self.get_project(project_id)
        if not project:
            return False
        if name and len(name) <= 30 and not any(p.name == name and p.id != project.id for p in self.projects.values()):
            project.name = name
        if description and len(description) <= 150:
            project.description = description
        return True

    def delete_project(self, project_id: str) -> bool:
        return self.projects.pop(project_id, None) is not None

    def get_project(self, project_id: str) -> Optional[Project]:
        return next((p for p in self.projects.values() if p.id.startswith(project_id)), None)

    def list_projects(self) -> List[Project]:
        return sorted(self.projects.values(), key=lambda p: p.created_at)
