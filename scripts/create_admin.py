
from app.database import SessionLocal
from app.models import User

def create_admin(email: str):
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email == email).first()

        if user is None:
            print("User not found")
            return

        if user.role == "admin":
            print("User is already an admin")
            return

        user.role = "admin"
        db.commit()

        print(f"{user.email} is now an admin")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    email = input("Enter the existing user's email: ").strip()
    create_admin(email)
