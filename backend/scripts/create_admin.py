import getpass

from sqlalchemy import select

from app.core.auth import hash_password
from app.core.database import SessionLocal
from app.models.user import User


def main():
    email = input("Admin email: ").strip().lower()
    password = getpass.getpass("Admin password: ")

    if len(password) < 14:
        raise SystemExit("Password too short (minimum 14 characters)")

    db = SessionLocal()
    try:
        existing = db.execute(
            select(User).where(User.email == email).limit(1)
        ).scalar_one_or_none()

        if existing:
            raise SystemExit("User already exists")

        user = User(
            email=email,
            password_hash=hash_password(password),
            is_active=True,
            is_admin=True,
            two_factor_enabled=False,
            two_factor_secret=None,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        print(f"Admin created: {user.email} ({user.id})")
    finally:
        db.close()


if __name__ == "__main__":
    main()