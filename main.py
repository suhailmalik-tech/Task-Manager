from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.db import Base, engine
from app.user.models import UserModel
from app.tasks.models import TaskModel
from app.user.router import user_routes
from app.tasks.router import task_routes

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management Application API",
    description="Backend API for Todo Task Management System with JWT Authentication",
    version="1.0.0"
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(user_routes)
app.include_router(task_routes)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Task Management API is running"}