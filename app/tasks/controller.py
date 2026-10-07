from typing import List, Union
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.tasks.dtos import TaskSchema, TaskUpdateSchema
from app.tasks.models import TaskModel
from app.user.models import UserModel

def create_task(body: TaskSchema, db: Session, user: UserModel) -> TaskModel:
    new_task = TaskModel(
        title=body.title,
        description=body.description,
        is_completed=body.is_completed,
        user_id=user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks(db: Session, user: UserModel) -> List[TaskModel]:
    return db.query(TaskModel).filter(TaskModel.user_id == user.id).all()

def get_one_task(task_id: int, db: Session, user: UserModel) -> TaskModel:
    task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

def update_task(body: Union[TaskSchema, TaskUpdateSchema], task_id: int, db: Session, user: UserModel) -> TaskModel:
    task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

def delete_task(task_id: int, db: Session, user: UserModel):
    task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.delete(task)
    db.commit()
    return None