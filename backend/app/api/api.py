from fastapi import APIRouter
from app.api.endpoints import auth, users, tasks, attendance, analytics, websockets, reports

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(websockets.router, tags=["websockets"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
