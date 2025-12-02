from sqlalchemy.orm import Session
from todo_list_app.models.task import Task, Status
from todo_list_app.config import MAX_NUMBER_OF_TASK
from todo_list_app.exceptions.repository_exceptions import LimitExceededError, NotFoundError

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, project_id: int, title: str, description: str = "", status: Status = Status.TODO, due_date: Optional[str] = None) -> Task:
        if self.db.query(Task).filter(Task.project_id == project_id).count() >= MAX_NUMBER_OF_TASK:
            raise LimitExceededError(f"حداکثر {MAX_NUMBER_OF_TASK} تسک در هر پروژه")
        task = Task(title=title, description=description, status=status, due_date=due_date, project_id=project_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Task:
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise NotFoundError("تسک پیدا نشد")
        return task

    def update(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[Status] = None, due_date: Optional[str] = None) -> Task:
        task = self.get_by_id(task_id)
        if title:
            task.title = title
        if description:
            task.description = description
        if status:
            task.status = status
        if due_date:
            task.due_date = due_date
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> None:
        task = self.get_by_id(task_id)
        self.db.delete(task)
        self.db.commit()

    def get_by_project(self, project_id: int) -> List[Task]:
        return self.db.query(Task).filter(Task.project_id == project_id).all()

    def get_all(self) -> List[Task]:
        return self.db.query(Task).all()