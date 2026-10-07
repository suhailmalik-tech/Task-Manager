from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.utils.db import Base

class UserModel(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False, index=True)
    hash_password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)

    tasks = relationship("TaskModel", back_populates="user", cascade="all, delete-orphan")