from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from todo_list_app.db.session import get_session
from todo_list_app.services.task_service import TaskService
from todo_list_app.api.controller_schemas.requests.tasks_request_schema import TaskCreateRequest, TaskUpdateRequest
from todo_list_app.api.controller_schemas.responses.tasks_response_schema import TaskResponse
from todo_list_app.models.task import Status as TaskStatus

router = APIRouter()

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreateRequest, db: Session = Depends(get_session)):
    service = TaskService(db)
    try:
        return service.create_task(task.project_id, task.title, task.description, TaskStatus(task.status), task.due_date)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/project/{project_id}", response_model=List[TaskResponse])
def list_tasks(project_id: int, db: Session = Depends(get_session)):
    service = TaskService(db)
    return service.list_tasks(project_id)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdateRequest, db: Session = Depends(get_session)):
    service = TaskService(db)
    try:
        updated = service.update_task(task_id, task.title, task.description, task.due_date)
        if task.status:
            service.update_task_status(task_id, TaskStatus(task.status))
        return updated
    except NotFoundError:
        raise HTTPException(status_code=404, detail="task not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(task_id: int, status: TaskStatus, db: Session = Depends(get_session)):
    service = TaskService(db)
    try:
        return service.update_task_status(task_id, status)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="task not found")

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_session)):
    service = TaskService(db)
    try:
        service.delete_task(task_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="تسک پیدا نشد")