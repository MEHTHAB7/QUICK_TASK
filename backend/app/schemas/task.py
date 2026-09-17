from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.schemas.user import User

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "Pending"
    priority: str = "Medium"
    due_date: Optional[datetime] = None
    assigned_to_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None

class TaskInDBBase(TaskBase):
    id: int
    created_by_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class Task(TaskInDBBase):
    assignee: Optional[User] = None
    creator: Optional[User] = None
