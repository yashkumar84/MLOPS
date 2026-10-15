"""FastAPI service: Placement Chance Predictor (trained on synthetic data, for learning)."""
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

FEATURES = ["cgpa", "dsa_problems", "projects", "internships", "communication", "backlogs"]
model = joblib.load("model/model.joblib")
app = FastAPI(title="Placement Chance Predictor")


class Student(BaseModel):
    cgpa: float = Field(..., ge=0, le=10, examples=[7.5])
    dsa_problems: int = Field(..., ge=0, le=5000, examples=[120])
    projects: int = Field(..., ge=0, le=50, examples=[2])
    internships: int = Field(..., ge=0, le=20, examples=[1])
    communication: float = Field(..., ge=1, le=10, examples=[7])
    backlogs: int = Field(..., ge=0, le=30, examples=[0])


def tips(s: Student) -> list[str]:
    out = []
    if s.dsa_problems < 150:
        out.append("Solve more DSA problems (aim for 150+ on LeetCode)")
    if s.projects < 3:
        out.append("Build 1-2 more projects and put them on GitHub")
    if s.internships < 1:
        out.append("Try to get at least one internship")
    if s.communication < 6:
        out.append("Practice mock interviews to improve communication")
    if s.backlogs > 0:
        out.append("Clear your backlogs; they hurt a lot")
    if s.cgpa < 7:
        out.append("Raise your CGPA where you still can")
    return out or ["Looking strong. Keep practicing and apply widely."]


@app.get("/", response_class=HTMLResponse)
def home():
    return Path("static/index.html").read_text(encoding="utf-8")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(s: Student):
    x = pd.DataFrame([[getattr(s, f) for f in FEATURES]], columns=FEATURES)
    chance = float(model.predict_proba(x)[0][1])
    return {"placement_chance_percent": round(chance * 100, 1), "tips": tips(s)}
