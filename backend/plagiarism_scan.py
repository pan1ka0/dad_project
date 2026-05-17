from difflib import SequenceMatcher

from database import SessionLocal
from models import Submission


def calculate_similarity(text1: str, text2: str) -> float:
    if not text1 or not text2:
        return 0.0

    similarity = SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    return round(similarity * 100, 2)


def run_plagiarism_scan():
    db = SessionLocal()

    try:
        submissions = db.query(Submission).all()

        if len(submissions) < 2:
            print("Not enough submissions to compare.")
            return

        print("Starting plagiarism scan...")
        print("-" * 40)

        found_suspicious = False

        for i in range(len(submissions)):
            for j in range(i + 1, len(submissions)):
                submission_a = submissions[i]
                submission_b = submissions[j]

                similarity = calculate_similarity(
                    submission_a.answer,
                    submission_b.answer
                )

                if similarity >= 70:
                    found_suspicious = True
                    print(
                        f"Suspicious similarity found: "
                        f"Submission {submission_a.id} and Submission {submission_b.id} "
                        f"are {similarity}% similar"
                    )

        if not found_suspicious:
            print("No suspicious submissions found.")

        print("-" * 40)
        print("Plagiarism scan completed.")

    finally:
        db.close()


if __name__ == "__main__":
    run_plagiarism_scan()