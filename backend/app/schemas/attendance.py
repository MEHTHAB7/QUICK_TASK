from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel
from app.schemas.user import User

class AttendanceBase(BaseModel):
    status: str = "Present"

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(AttendanceBase):
    check_out: Optional[datetime] = None

class AttendanceInDBBase(AttendanceBase):
    id: int
    user_id: int
    date: date
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}

class Attendance(AttendanceInDBBase):
    user: Optional[User] = None
