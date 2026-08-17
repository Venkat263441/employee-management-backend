from .database import SessionLocal
from . import models
from .security import hash_password


def create_admin():
    db = SessionLocal()

    try:
        existing_admin = (
            db.query(models.User)
            .filter(models.User.email == "admin@gmail.com")
            .first()
        )

        if existing_admin:
            print("Admin already exists")
            return

        admin = models.User(
            name="Admin",
            email="admin@gmail.com",
            password_hash=hash_password("admin123"),
            role="admin"
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("Admin created successfully")
        print("Email: admin@gmail.com")
        print("Password: admin123")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()