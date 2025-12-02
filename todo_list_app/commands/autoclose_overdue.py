from datetime import datetime
from todo_list_app.db.session import get_session
from todo_list_app.services.task_service import TaskService
from todo_list_app.models.task import Status as TaskStatus

def autoclose_overdue():
    db = next(get_session())
    service = TaskService(db)
    tasks = service.repo.get_all()
    for task in tasks:
        if task.due_date and task.status != TaskStatus.DONE:
            due = datetime.strptime(task.due_date, "%Y-%m-%d").date()
            if due < datetime.now().date():
                service.update_task_status(task.id, TaskStatus.DONE)
    db.close()