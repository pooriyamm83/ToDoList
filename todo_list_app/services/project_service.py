from sqlalchemy.orm import Session
from todo_list_app.repositories.project_repository import ProjectRepository
from todo_list_app.exceptions.service_exceptions import ValidationError

class ProjectService:
    def __init__(self, db: Session):
        self.repo = ProjectRepository(db)

    def create_project(self, name: str, description: str = "") -> Project:
        if len(name) > 30:
            raise ValidationError("نام پروژه حداکثر ۳۰ کاراکتر")
        if len(description) > 150:
            raise ValidationError("توضیحات حداکثر ۱۵۰ کاراکتر")
        return self.repo.create(name, description)

    def list_projects(self) -> List[Project]:
        return self.repo.list_all()

    def update_project(self, project_id: int, name: Optional[str] = None, description: Optional[str] = None) -> Project:
        if name and len(name) > 30:
            raise ValidationError("نام جدید حداکثر ۳۰ کاراکتر")
        if description and len(description) > 150:
            raise ValidationError("توضیحات جدید حداکثر ۱۵۰ کاراکتر")
        return self.repo.update(project_id, name, description)

    def delete_project(self, project_id: int) -> None:
        self.repo.delete(project_id)