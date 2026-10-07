from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.user import controller
from app.user.dtos import UserSchema, UserResponseSchema, LoginSchema
from app.user.models import UserModel
from app.utils.db import get_db
from app.utils.helpers import is_authenticated

user_routes = APIRouter(prefix="/user", tags=["User"])

@user_routes.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def register(body: UserSchema, db: Session = Depends(get_db)):
    return controller.register(body, db)

@user_routes.post("/login", status_code=status.HTTP_200_OK)
def login(body: LoginSchema, db: Session = Depends(get_db)):
    return controller.login_user(body, db)

@user_routes.get("/is_auth", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
def is_auth(current_user: UserModel = Depends(is_authenticated)):
    return current_user
