from database import SessionLocal, Base, engine
from models import User, Course, Assignment, Submission
from auth import hash_password


Base.metadata.create_all(bind=engine)


def seed_database():
    db = SessionLocal()

    try:
        # Clear old data
        db.query(Submission).delete()
        db.query(Assignment).delete()
        db.query(Course).delete()
        db.query(User).delete()
        db.commit()

        # =========================
        # USERS
        # =========================

        teacher1 = User(
            full_name="Dr. Sarvar Abdullaev",
            email="sarvar.teacher@gmail.com",
            password=hash_password("123456"),
            role="teacher"
        )

        teacher2 = User(
            full_name="Leonel Messi",
            email="messi.teacher@gmail.com",
            password=hash_password("123456"),
            role="teacher"
        )

        student1 = User(
            full_name="Javanessa Panikovna",
            email="javohir.student@gmail.com",
            password=hash_password("123456"),
            role="student"
        )

        student2 = User(
            full_name="Sabina Valiyeva",
            email="sabina.student@gmail.com",
            password=hash_password("123456"),
            role="student"
        )

        student3 = User(
            full_name="Erna Dinozavr",
            email="erna.student@gmail.com",
            password=hash_password("123456"),
            role="student"
        )

        student4 = User(
            full_name="Sherzod Inoyatov",
            email="sherzod.student@gmail.com",
            password=hash_password("123456"),
            role="student"
        )

        db.add_all([
            teacher1,
            teacher2,
            student1,
            student2,
            student3,
            student4
        ])
        db.commit()

        db.refresh(teacher1)
        db.refresh(teacher2)
        db.refresh(student1)
        db.refresh(student2)
        db.refresh(student3)
        db.refresh(student4)

        # =========================
        # COURSES
        # =========================

        course1 = Course(
            title="Database Design",
            description="Introduction to relational databases, ER diagrams, and SQL.",
            teacher_id=teacher1.id
        )

        course2 = Course(
            title="Backend Development",
            description="Building REST APIs using FastAPI and PostgreSQL.",
            teacher_id=teacher1.id
        )

        course3 = Course(
            title="System Design Basics",
            description="Caching, rate limiting, WebSockets, and batch processing.",
            teacher_id=teacher2.id
        )

        db.add_all([course1, course2, course3])
        db.commit()

        db.refresh(course1)
        db.refresh(course2)
        db.refresh(course3)

        # =========================
        # ASSIGNMENTS
        # =========================

        assignment1 = Assignment(
            title="ER Diagram Task",
            description="Create an ER diagram for a university LMS system.",
            course_id=course1.id
        )

        assignment2 = Assignment(
            title="SQL Normalization Task",
            description="Explain 1NF, 2NF, and 3NF using examples.",
            course_id=course1.id
        )

        assignment3 = Assignment(
            title="FastAPI CRUD API",
            description="Create CRUD endpoints for a small backend system.",
            course_id=course2.id
        )

        assignment4 = Assignment(
            title="Caching Explanation",
            description="Explain how Redis cache improves read performance.",
            course_id=course3.id
        )

        db.add_all([
            assignment1,
            assignment2,
            assignment3,
            assignment4
        ])
        db.commit()

        db.refresh(assignment1)
        db.refresh(assignment2)
        db.refresh(assignment3)
        db.refresh(assignment4)

        # =========================
        # SUBMISSIONS
        # =========================

        submission1 = Submission(
            answer="An ER diagram shows entities, attributes, and relationships between tables in a database system.",
            student_id=student1.id,
            assignment_id=assignment1.id,
            grade=90
        )

        submission2 = Submission(
            answer="An ER diagram represents entities, their attributes, and relationships in the database design.",
            student_id=student2.id,
            assignment_id=assignment1.id,
            grade=88
        )

        submission3 = Submission(
            answer="First normal form removes repeating groups. Second normal form removes partial dependencies. Third normal form removes transitive dependencies.",
            student_id=student3.id,
            assignment_id=assignment2.id,
            grade=92
        )

        submission4 = Submission(
            answer="FastAPI can be used to create REST endpoints such as GET, POST, PUT, and DELETE for CRUD operations.",
            student_id=student4.id,
            assignment_id=assignment3.id,
            grade=85
        )

        submission5 = Submission(
            answer="Redis improves performance by storing frequently requested data in memory, so repeated reads are faster.",
            student_id=student1.id,
            assignment_id=assignment4.id,
            grade=95
        )

        submission6 = Submission(
            answer="Redis cache stores popular data in memory and helps reduce repeated database queries.",
            student_id=student2.id,
            assignment_id=assignment4.id,
            grade=None
        )

        db.add_all([
            submission1,
            submission2,
            submission3,
            submission4,
            submission5,
            submission6
        ])
        db.commit()

        print("Database seeded successfully!")
        print("Sample login password for all users: 123456")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()