from pydantic import BaseModel
from typing import Optional


# =========================
# USER SCHEMAS
# =========================

class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    role: str = "student"


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str

    class Config:
        from_attributes = True


# =========================
# COURSE SCHEMAS
# =========================

class CourseCreate(BaseModel):
    title: str
    description: str
    teacher_id: int


class CourseUpdate(BaseModel):
    title: str
    description: str
    teacher_id: int


class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    teacher_id: int

    class Config:
        from_attributes = True


# =========================
# ASSIGNMENT SCHEMAS
# =========================

class AssignmentCreate(BaseModel):
    title: str
    description: str
    course_id: int


class AssignmentResponse(BaseModel):
    id: int
    title: str
    description: str
    course_id: int

    class Config:
        from_attributes = True


# =========================
# SUBMISSION SCHEMAS
# =========================

class SubmissionCreate(BaseModel):
    answer: str
    student_id: int
    assignment_id: int


class SubmissionResponse(BaseModel):
    id: int
    answer: str
    student_id: int
    assignment_id: int
    grade: Optional[int] = None

    class Config:
        from_attributes = True


class GradeSubmission(BaseModel):
    grade: int