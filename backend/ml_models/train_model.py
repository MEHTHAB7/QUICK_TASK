import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import os

def generate_mock_data(num_samples=1000):
    np.random.seed(42)
    # Features: tasks_completed, hours_worked, lines_of_code, bugs_fixed, meetings_attended
    data = {
        'tasks_completed': np.random.randint(1, 20, num_samples),
        'hours_worked': np.random.uniform(30, 60, num_samples),
        'lines_of_code': np.random.randint(100, 2000, num_samples),
        'bugs_fixed': np.random.randint(0, 10, num_samples),
        'meetings_attended': np.random.randint(0, 15, num_samples)
    }
    df = pd.DataFrame(data)
    
    # Target: Productivity Score (0-100)
    # Higher tasks, LOC, bugs fixed -> higher score. Higher meetings -> slightly lower score.
    base_score = 50
    score = (
        base_score 
        + (df['tasks_completed'] * 1.5)
        + (df['lines_of_code'] * 0.01)
        + (df['bugs_fixed'] * 2.0)
        - (df['meetings_attended'] * 1.0)
    )
    # Add some noise
    score += np.random.normal(0, 5, num_samples)
    
    # Clip to 0-100
    df['productivity_score'] = np.clip(score, 0, 100)
    return df

def train():
    print("Generating mock data...")
    df = generate_mock_data()
    
    X = df.drop('productivity_score', axis=1)
    y = df['productivity_score']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Model trained. Mean Squared Error: {mse:.2f}")
    
    # Save model
    os.makedirs('ml_models', exist_ok=True)
    joblib.dump(model, 'ml_models/productivity_model.joblib')
    print("Model saved to ml_models/productivity_model.joblib")

if __name__ == "__main__":
    train()
