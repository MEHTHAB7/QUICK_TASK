from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_task
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.schemas.user import User

router = APIRouter()

@router.get("/", response_model=List[Task])
def read_tasks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    # If admin/manager, return all tasks. Otherwise, return only tasks assigned to the user.
    if current_user.role in ["admin", "manager"]:
        tasks = crud_task.get_tasks(db, skip=skip, limit=limit)
    else:
        tasks = crud_task.get_tasks_by_user(db, user_id=current_user.id)
    return tasks

@router.post("/", response_model=Task)
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    task_in: TaskCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    # Anyone can create a task in this basic implementation
    task = crud_task.create_task(db, task=task_in, creator_id=current_user.id)
    return task

@router.put("/{task_id}", response_model=Task)
def update_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int,
    task_in: TaskUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    task = crud_task.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role not in ["admin", "manager"] and task.assigned_to_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    task = crud_task.update_task(db, db_task=task, task_update=task_in)
    return task

@router.delete("/{task_id}")
def delete_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int,
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    success = crud_task.delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
