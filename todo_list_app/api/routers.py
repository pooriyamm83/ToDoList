from fastapi import APIRouter
from todo_list_app.api.controllers.projects_controller import router as projects_router
from todo_list_app.api.controllers.tasks_controller import router as tasks_router

router = APIRouter()

router.include_router(projects_router, prefix="/projects", tags=["projects"])
router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])