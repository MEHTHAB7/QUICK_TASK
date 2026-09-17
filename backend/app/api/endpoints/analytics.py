import os
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.user import User
import joblib
import pandas as pd

router = APIRouter()

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'ml_models', 'productivity_model.joblib')

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Could not load ML model: {e}")

@router.post("/predict-productivity")
def predict_productivity(
    data: Dict[str, float],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    if model is None:
        raise HTTPException(status_code=503, detail="ML Model is not loaded or available.")
    
    try:
        # Expected features: tasks_completed, hours_worked, lines_of_code, bugs_fixed, meetings_attended
        df = pd.DataFrame([data])
        prediction = model.predict(df)[0]
        return {"productivity_score": round(prediction, 2)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@router.get("/dashboard-stats")
def get_dashboard_stats(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    # Mock aggregated data for the admin dashboard
    return {
        "total_employees": 124,
        "active_tasks": 45,
        "completed_tasks": 312,
        "avg_productivity_score": 82.4,
        "weekly_trends": [
            {"day": "Mon", "score": 78},
            {"day": "Tue", "score": 82},
            {"day": "Wed", "score": 85},
            {"day": "Thu", "score": 81},
            {"day": "Fri", "score": 86},
        ],
        "department_performance": [
            {"name": "Engineering", "value": 88},
            {"name": "Design", "value": 82},
            {"name": "Marketing", "value": 79},
            {"name": "Sales", "value": 85},
        ]
    }
