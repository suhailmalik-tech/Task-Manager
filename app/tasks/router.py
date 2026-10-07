from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.tasks import controller
from app.tasks.dtos import TaskSchema, TaskUpdateSchema, TaskResponseSchema
from app.utils.db import get_db
from app.user.models import UserModel
from app.utils.helpers import is_authenticated

task_routes = APIRouter(prefix="/tasks", tags=["Tasks"])

@task_routes.post("/create", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
def create_task(
    body: TaskSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated)
):
    return controller.create_task(body, db, user)

@task_routes.get("/get_tasks", response_model=List[TaskResponseSchema], status_code=status.HTTP_200_OK)
def get_all_tasks(
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated)
):
    return controller.get_tasks(db, user)

@task_routes.get("/get_one/{task_id}", response_model=TaskResponseSchema, status_code=status.HTTP_200_OK)
@task_routes.get("/get_one", response_model=TaskResponseSchema, status_code=status.HTTP_200_OK, include_in_schema=False)
def get_one_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated)
):
    return controller.get_one_task(task_id, db, user)

@task_routes.put("/update_task/{task_id}", response_model=TaskResponseSchema, status_code=status.HTTP_200_OK)
def update_task(
    body: TaskSchema,
    task_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated)
):
    return controller.update_task(body, task_id, db, user)

@task_routes.delete("/delete_task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated)
):
    return controller.delete_task(task_id, db, user)