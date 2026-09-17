from typing import Any, List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_attendance
from app.schemas.attendance import Attendance
from app.schemas.user import User

router = APIRouter()

@router.get("/", response_model=List[Attendance])
def read_attendances(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    # Basic implementation: users see their own attendance.
    # A real enterprise app would allow managers to see their team's attendance.
    if current_user.role == "admin":
        # We need a get_all_attendances crud for admin, but for simplicity, returning user's for now
        pass
    attendances = crud_attendance.get_attendances_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return attendances

@router.post("/check-in", response_model=Attendance)
def check_in(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    attendance = crud_attendance.check_in(db, user_id=current_user.id)
    return attendance

@router.post("/check-out", response_model=Attendance)
def check_out(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    today = date.today()
    attendance = crud_attendance.get_attendance_by_user_date(db, user_id=current_user.id, date=today)
    if not attendance:
        raise HTTPException(status_code=400, detail="You must check-in first.")
    if attendance.check_out:
        raise HTTPException(status_code=400, detail="Already checked out.")
    attendance = crud_attendance.check_out(db, db_attendance=attendance)
    return attendance
