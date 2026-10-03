from fastapi import FastAPI
from app.utils.db import Base, engine
from app.tasks.models import TaskModel
from app.tasks.router import task_routes

Base.metadata.create_all(engine)


app = FastAPI(title="This is my Task Management Application")

app.include_router(task_routes)