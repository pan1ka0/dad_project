from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session

import io
import csv
import os
import json

import redis
from dotenv import load_dotenv

from database import Base, engine, get_db
from models import User, Course, Assignment, Submission

from schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    CourseCreate,
    CourseResponse,
    CourseUpdate,
    AssignmentCreate,
    AssignmentResponse,
    SubmissionCreate,
    SubmissionResponse,
    GradeSubmission
)

from auth import hash_password, verify_password, create_token
from rate_limiter import login_rate_limiter

# =========================
# APP + DATABASE SETUP
# =========================

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="University LMS Lite API")


# =========================
# REDIS SETUP
# =========================

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    print("Redis connected successfully")
except Exception:
    redis_client = None
    print("Redis is not available. Using PostgreSQL only.")


def clear_courses_cache():
    if redis_client:
        redis_client.delete("courses_cache")


# =========================
# WEBSOCKET CHAT MANAGER
# =========================

class ChatManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, course_id: int, websocket: WebSocket):
        await websocket.accept()

        if course_id not in self.active_connections:
            self.active_connections[course_id] = []

        self.active_connections[course_id].append(websocket)

    def disconnect(self, course_id: int, websocket: WebSocket):
        if course_id in self.active_connections:
            if websocket in self.active_connections[course_id]:
                self.active_connections[course_id].remove(websocket)

            if len(self.active_connections[course_id]) == 0:
                del self.active_connections[course_id]

    async def send_message_to_course(self, course_id: int, message: str):
        if course_id in self.active_connections:
            for connection in self.active_connections[course_id]:
                await connection.send_text(message)


chat_manager = ChatManager()


# =========================
# HOME + CACHE STATUS
# =========================

@app.get("/")
def home():
    return {"message": "University LMS Lite API is running"}


@app.get("/cache/status")
def cache_status():
    if redis_client:
        return {
            "redis": "connected",
            "message": "Redis cache is available"
        }

    return {
        "redis": "not connected",
        "message": "Backend is using PostgreSQL only"
    }


# =========================
# AUTH ENDPOINTS
# =========================

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


@app.post("/login")
def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    client_ip = request.client.host

    if not login_rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts. Please try again later."
        )

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_token({
        "user_id": db_user.id,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# =========================
# USER ENDPOINTS
# =========================

@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get("/users/students", response_model=list[UserResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(User).filter(User.role == "student").all()


@app.get("/users/teachers", response_model=list[UserResponse])
def get_teachers(db: Session = Depends(get_db)):
    return db.query(User).filter(User.role == "teacher").all()


# =========================
# COURSE ENDPOINTS
# =========================

@app.post("/courses", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    teacher = db.query(User).filter(User.id == course.teacher_id).first()

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    if teacher.role != "teacher":
        raise HTTPException(status_code=400, detail="User is not a teacher")

    new_course = Course(
        title=course.title,
        description=course.description,
        teacher_id=course.teacher_id
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    clear_courses_cache()

    return new_course


@app.get("/courses", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    if redis_client:
        cached_courses = redis_client.get("courses_cache")

        if cached_courses:
            return json.loads(cached_courses)

    courses = db.query(Course).all()

    courses_data = [
        {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "teacher_id": course.teacher_id
        }
        for course in courses
    ]

    if redis_client:
        redis_client.setex(
            "courses_cache",
            60,
            json.dumps(courses_data)
        )

    return courses_data


@app.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course


@app.put("/courses/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course_data: CourseUpdate, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    teacher = db.query(User).filter(User.id == course_data.teacher_id).first()

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    if teacher.role != "teacher":
        raise HTTPException(status_code=400, detail="User is not a teacher")

    course.title = course_data.title
    course.description = course_data.description
    course.teacher_id = course_data.teacher_id

    db.commit()
    db.refresh(course)

    clear_courses_cache()

    return course


@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(course)
    db.commit()

    clear_courses_cache()

    return {"message": "Course deleted successfully"}


# =========================
# ASSIGNMENT ENDPOINTS
# =========================

@app.post("/assignments", response_model=AssignmentResponse)
def create_assignment(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == assignment.course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    new_assignment = Assignment(
        title=assignment.title,
        description=assignment.description,
        course_id=assignment.course_id
    )

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return new_assignment


@app.get("/assignments", response_model=list[AssignmentResponse])
def get_assignments(db: Session = Depends(get_db)):
    return db.query(Assignment).all()


@app.get("/assignments/{assignment_id}", response_model=AssignmentResponse)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    return assignment


@app.get("/courses/{course_id}/assignments", response_model=list[AssignmentResponse])
def get_course_assignments(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return db.query(Assignment).filter(Assignment.course_id == course_id).all()


@app.delete("/assignments/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    db.delete(assignment)
    db.commit()

    return {"message": "Assignment deleted successfully"}


# =========================
# SUBMISSION ENDPOINTS
# =========================

@app.post("/submissions", response_model=SubmissionResponse)
def create_submission(submission: SubmissionCreate, db: Session = Depends(get_db)):
    student = db.query(User).filter(User.id == submission.student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if student.role != "student":
        raise HTTPException(status_code=400, detail="User is not a student")

    assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    new_submission = Submission(
        answer=submission.answer,
        student_id=submission.student_id,
        assignment_id=submission.assignment_id,
        grade=None
    )

    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    return new_submission


@app.get("/submissions", response_model=list[SubmissionResponse])
def get_submissions(db: Session = Depends(get_db)):
    return db.query(Submission).all()


@app.get("/submissions/{submission_id}", response_model=SubmissionResponse)
def get_submission(submission_id: int, db: Session = Depends(get_db)):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    return submission


@app.get("/assignments/{assignment_id}/submissions", response_model=list[SubmissionResponse])
def get_assignment_submissions(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    return db.query(Submission).filter(Submission.assignment_id == assignment_id).all()


@app.put("/submissions/{submission_id}/grade", response_model=SubmissionResponse)
def grade_submission(
    submission_id: int,
    grade_data: GradeSubmission,
    db: Session = Depends(get_db)
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    if grade_data.grade < 0 or grade_data.grade > 100:
        raise HTTPException(status_code=400, detail="Grade must be between 0 and 100")

    submission.grade = grade_data.grade

    db.commit()
    db.refresh(submission)

    return submission


@app.delete("/submissions/{submission_id}")
def delete_submission(submission_id: int, db: Session = Depends(get_db)):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    db.delete(submission)
    db.commit()

    return {"message": "Submission deleted successfully"}


# =========================
# GRADE EXPORT ENDPOINT
# =========================

@app.get("/grades/export")
def export_grades(db: Session = Depends(get_db)):
    submissions = db.query(Submission).all()

    lines = []
    lines.append("ID,Student,Course,Assignment,Answer,Grade,Status")

    for submission in submissions:
        student = db.query(User).filter(User.id == submission.student_id).first()
        assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()

        course = None
        if assignment:
            course = db.query(Course).filter(Course.id == assignment.course_id).first()

        student_name = student.full_name if student else "Unknown student"
        course_title = course.title if course else "Unknown course"
        assignment_title = assignment.title if assignment else "Unknown assignment"
        answer = submission.answer if submission.answer else ""
        grade = str(submission.grade) if submission.grade is not None else "Not graded"
        status = "Graded" if submission.grade is not None else "Pending"

        # Clean text so CSV does not break
        student_name = student_name.replace(",", " ")
        course_title = course_title.replace(",", " ")
        assignment_title = assignment_title.replace(",", " ")
        answer = answer.replace("\n", " ").replace("\r", " ").replace(",", " ")

        line = f"{submission.id},{student_name},{course_title},{assignment_title},{answer},{grade},{status}"
        lines.append(line)

    csv_content = "\n".join(lines)

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=grades_report.csv"
        }
    )

# =========================
# WEBSOCKET LIVE CHAT
# =========================

@app.websocket("/ws/chat/{course_id}")
async def websocket_chat(websocket: WebSocket, course_id: int):
    await chat_manager.connect(course_id, websocket)

    try:
        while True:
            message = await websocket.receive_text()
            full_message = f"Course {course_id}: {message}"
            await chat_manager.send_message_to_course(course_id, full_message)

    except WebSocketDisconnect:
        chat_manager.disconnect(course_id, websocket)
