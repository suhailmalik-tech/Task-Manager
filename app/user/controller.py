from app.user.dtos import UserSchema,LoginSchema
from sqlalchemy.orm import Session
from app.user.models import UserModel
from app.utils.settings import settings
from fastapi import HTTPException, status , Request
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta


import jwt 

password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)



def register(body:UserSchema, db:Session):
    is_user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user:
        raise HTTPException(400, detail="Email already exist...")

    is_user = db.query(UserModel).filter(UserModel.usernme == body.username).first()
    if is_user:

        raise HTTPException(400, detail="Username already exist...")

    hash_password = get_password_hash(body.password)

    new_user = UserModel(
        name = body.name,
        username = body.username,
        hash_password = hash_password,
        email = body.email,
    )
    db.add(new_user)
    db.commit()
    db.refresh()

    return new_user



def login_user(body:LoginSchema, db:Session):
    is_email = db.query(UserModel).filter(UserModel.email == body.email).first()
    if not is_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You Entered Wrong Email")

    if not verify_password(body.password, is_email.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail ="Your Password is Incorrect")

    exp_time = datetime.now() + timedelta(minutes=settings.EXPIRE_MINUTES)
    token = jwt.encode({"_id:user.id"}, settings.SECRET_KEY, settings.ALGORITHM )


    
    return {"token": token}


def is_authenticated(request:Request, db:Session):
    try:
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "You are Unauthorized")
                
        
           
        token = token.split(" ")[-1]
        
        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id = data.get("_id")
          
        
        user = db.query(UserModel).filter(UserModel.id == user.id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized")
        return user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized")
        
    

