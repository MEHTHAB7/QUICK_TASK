from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    status = Column(String, default="Pending") # Pending, In Progress, Completed, Delayed
    priority = Column(String, default="Medium") # Low, Medium, High, Critical
    due_date = Column(DateTime(timezone=True))
    
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    assignee = relationship("User", foreign_keys=[assigned_to_id], backref="assigned_tasks")
    creator = relationship("User", foreign_keys=[created_by_id], backref="created_tasks")
