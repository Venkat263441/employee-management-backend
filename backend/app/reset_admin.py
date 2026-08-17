from .database import SessionLocal
from . import models
from .security import hash_password


def reset_admin_password():
    db = SessionLocal()

    try:
        admin = (
            db.query(models.User)
            .filter(models.User.email == "admin@gmail.com")
            .first()
        )

        if admin is None:
            print("Admin user not found")
            return

        admin.password_hash = hash_password("admin123")

        db.commit()

        print("Admin password reset successfully")
        print("Email: admin@gmail.com")
        print("New password: admin123")

    finally:
        db.close()


if __name__ == "__main__":
    reset_admin_password()