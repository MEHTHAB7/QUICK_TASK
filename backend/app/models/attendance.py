from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    check_in = Column(DateTime(timezone=True))
    check_out = Column(DateTime(timezone=True))
    status = Column(String, default="Present") # Present, Absent, Late, Half-day
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="attendance_records")
