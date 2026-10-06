
from app.user.dtos import UserSchema,LoginSchema
from sqlalchemy.orm import Session
from app.user.models import UserModel
from app.utils.settings import settings
from fastapi import HTTPException, status , Request
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta

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
        
    