from pydantic import BaseModel, ConfigDict, EmailStr

class UserSchema(BaseModel):
    name: str
    username: str
    password: str
    email: EmailStr

class UserResponseSchema(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    
