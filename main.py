from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
import os

app = FastAPI(title="Student Performance API")

# Load model from root directory
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Student.pkl"))

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

label_map = {0: "Average", 1: "Excellent", 2: "Good", 3: "Poor"}

class StudentInput(BaseModel):
    study_hours: float
    attendance: float
    assignments: float
    exam_score: float

@app.post("/predict")
def predict(data: StudentInput):
    features = np.array([[data.study_hours, data.attendance, data.assignments, data.exam_score]])
    
    prediction = model.predict(features)[0]
    
    response = {
        "prediction_code": int(prediction),
        "prediction_label": label_map.get(int(prediction), f"Class {prediction}")
    }
    
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(features)[0].tolist()
        response["probabilities"] = {label_map.get(i, f"Class {i}"): prob for i, prob in enumerate(probs)}
        
    return response