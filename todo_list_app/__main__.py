# app/main.py
from fastapi import FastAPI
from todo_list_app.api.routers import router

app = FastAPI(
    title="ToDoList API",
    description="Phase 3 - Web API for ToDoList",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "ToDoList API - Visit /docs for Swagger UI"}