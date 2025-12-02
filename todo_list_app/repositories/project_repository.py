# app/repositories/project_repository.py
from sqlalchemy.orm import Session
from todo_list_app.models.project import Project
from todo_list_app.config import MAX_NUMBER_OF_PROJECT
from todo_list_app.exceptions.repository_exceptions import DuplicateError, LimitExceededError, NotFoundError

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, description: str = "") -> Project:
        if self.db.query(Project).count() >= MAX_NUMBER_OF_PROJECT:
            raise LimitExceededError(f"atmost {MAX_NUMBER_OF_PROJECT} projects allowed")
        if self.db.query(Project).filter(Project.name == name).first():
            raise DuplicateError("duplicate project name")
        project = Project(name=name, description=description)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_by_id(self, project_id: int) -> Project:
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundError("new project was not found")
        return project

    def update(self, project_id: int, name: Optional[str] = None, description: Optional[str] = None) -> Project:
        project = self.get_by_id(project_id)
        if name:
            if self.db.query(Project).filter(Project.name == name, Project.id != project_id).first():
                raise DuplicateError("duplicate newname")
            project.name = name
        if description:
            project.description = description
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project_id: int) -> None:
        project = self.get_by_id(project_id)
        self.db.delete(project)
        self.db.commit()

    def list_all(self) -> List[Project]:
        return self.db.query(Project).order_by(Project.created_at).all()