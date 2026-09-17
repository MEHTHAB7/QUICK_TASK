from typing import List, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate

def get_attendance(db: Session, attendance_id: int) -> Optional[Attendance]:
    return db.query(Attendance).filter(Attendance.id == attendance_id).first()

def get_attendance_by_user_date(db: Session, user_id: int, date: date) -> Optional[Attendance]:
    return db.query(Attendance).filter(
        Attendance.user_id == user_id, 
        Attendance.date == date
    ).first()

def get_attendances_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Attendance]:
    return db.query(Attendance).filter(Attendance.user_id == user_id).order_by(Attendance.date.desc()).offset(skip).limit(limit).all()

def check_in(db: Session, user_id: int) -> Attendance:
    today = date.today()
    existing = get_attendance_by_user_date(db, user_id, today)
    if existing:
        return existing
    
    db_attendance = Attendance(
        user_id=user_id,
        date=today,
        check_in=datetime.now(),
        status="Present"
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def check_out(db: Session, db_attendance: Attendance) -> Attendance:
    db_attendance.check_out = datetime.now()
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance
