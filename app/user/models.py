from sqlalchemy import Column, String , Integer, DateTime, Boolean
from app.utils.db import Base

class UserModel(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    usernme = Column(String)
    hash_password = Column(String, nullable=False)
    email = Column(String)