from .database import SessionLocal
from . import models
from .security import hash_password


def setup_admin():
    db = SessionLocal()

    try:
        admin = (
            db.query(models.User)
            .filter(models.User.email == "admin@gmail.com")
            .first()
        )

        if admin is None:
            admin = models.User(
                name="Admin",
                email="admin@gmail.com",
                password_hash=hash_password("admin123"),
                role="admin",
                is_active=True
            )

            db.add(admin)
            db.commit()
            db.refresh(admin)

            print("Admin created successfully")

        else:
            admin.password_hash = hash_password("admin123")
            admin.role = "admin"
            admin.is_active = True

            db.commit()

            print("Admin already existed - password reset successfully")

        print("Email: admin@gmail.com")
        print("Password: admin123")

    except Exception as e:
        db.rollback()
        print(f"Admin setup failed: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    setup_admin()