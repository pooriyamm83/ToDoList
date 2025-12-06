from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from todo_list_app.db.session import get_session
from todo_list_app.services.project_service import ProjectService
from todo_list_app.api.controller_schemas.requests.projects_request_schema import ProjectCreateRequest, ProjectUpdateRequest
from todo_list_app.api.controller_schemas.responses.projects_response_schema import ProjectResponse

router = APIRouter()

@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(project: ProjectCreateRequest, db: Session = Depends(get_session)):
    service = ProjectService(db)
    try:
        return service.create_project(project.name, project.description)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_session)):
    service = ProjectService(db)
    return service.list_projects()

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdateRequest, db: Session = Depends(get_session)):
    service = ProjectService(db)
    try:
        updated = service.update_project(project_id, project.name, project.description)
        return updated
    except NotFoundError:
        raise HTTPException(status_code=404, detail="project not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_session)):
    service = ProjectService(db)
    try:
        service.delete_project(project_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="project not found")