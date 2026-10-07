from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.user.dtos import UserSchema, LoginSchema
from app.user.models import UserModel
from app.utils.helpers import verify_password, get_password_hash, create_access_token, is_authenticated

def register(body: UserSchema, db: Session) -> UserModel:
    existing_email = db.query(UserModel).filter(UserModel.email == body.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist...")

    existing_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exist...")

    hashed_pw = get_password_hash(body.password)

    new_user = UserModel(
        name=body.name,
        username=body.username,
        hash_password=hashed_pw,
        email=body.email,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login_user(body: LoginSchema, db: Session):
    user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You Entered Wrong Email")

    if not verify_password(body.password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your Password is Incorrect")

    token = create_access_token(user.id)

    return {"token": token, "access_token": token, "token_type": "bearer"}
