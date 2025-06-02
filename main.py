from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List

app = FastAPI()

GRADE_MAPPING = {
    "A+": 4.5,
    "A0": 4.0,
    "B+": 3.5,
    "B0": 3.0,
    "C+": 2.5,
    "C0": 2.0,
    "D+": 1.5,
    "D0": 1.0,
    "F": 0.0
}

class Course(BaseModel):
    course_code: str
    course_name: str
    credits: int
    grade: str

    @validator("grade")
    def validate_grade(cls, v):
        if v not in GRADE_MAPPING:
            raise ValueError(f"Invalid grade: {v}")
        return v

class StudentRequest(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

class StudentSummary(BaseModel):
    student_id: str
    name: str
    gpa: float
    total_credits: int

@app.post("/score")
def calculate_gpa(data: StudentRequest):
    total_score = 0
    total_credits = 0
    for course in data.courses:
        grade_score = GRADE_MAPPING[course.grade]
        total_score += grade_score * course.credits
        total_credits += course.credits
    gpa = round(total_score / total_credits, 2)
    return {"student_summary": StudentSummary(
        student_id=data.student_id,
        name=data.name,
        gpa=gpa,
        total_credits=total_credits
    )}
