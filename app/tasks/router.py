from fastapi import APIRouter, Depends
from app.tasks import controller
from app.tasks.dtos import TaskSchema
from app.utils.db import get_db

task_routes = APIRouter(prefix="/tasks")


@task_routes.post("/create")
def create_task(body:TaskSchema, db = Depends(get_db)):
    return controller.create_task(body, db)


@task_routes.get("/get_tasks")
def get_all_tasks(db=Depends(get_db)):
    return controller.get_tasks(db)

@task_routes.get("/get_one")
def get_one_task(task_id:int, db = Depends(get_db)):
    return controller.get_one_task(task_id, db)


@task_routes.put("/update_task/{task_id}")
def update_task(body:TaskSchema, task_id:int, db=Depends(get_db)):
    return controller.update_task(body, task_id, db)


@task_routes.delete("/delete_task/{task_id}")
def delete_task( task_id:int, db=Depends(get_db)):
    return controller.delete_task(task_id, db)