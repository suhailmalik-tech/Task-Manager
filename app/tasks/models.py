from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.db import Base

class TaskModel(Base):
    __tablename__ = "user_tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("user_table.id", ondelete="CASCADE"), nullable=False)

    user = relationship("UserModel", back_populates="tasks")