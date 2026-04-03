import getpass
import sys

from pydantic import EmailStr, ValidationError, TypeAdapter
from sqlalchemy import select

from app.core.auth import hash_password
from app.core.database import SessionLocal
from app.models.user import User

MIN_PASSWORD_LENGTH = 14
email_adapter = TypeAdapter(EmailStr)


def prompt_email() -> str:
    raw = input("Admin email: ").strip().lower()
    try:
        return str(email_adapter.validate_python(raw))
    except ValidationError as exc:
        raise SystemExit(f"Invalid email address: {exc.errors()[0]['msg']}")


def prompt_password() -> str:
    password = getpass.getpass(f"Admin password (min {MIN_PASSWORD_LENGTH} chars): ")
    confirm = getpass.getpass("Confirm password: ")

    if password != confirm:
        raise SystemExit("Passwords do not match")

    if len(password) < MIN_PASSWORD_LENGTH:
        raise SystemExit(
            f"Password too short (minimum {MIN_PASSWORD_LENGTH} characters)"
        )

    return password


def main() -> None:
    print("Create a new admin user")
    print("-" * 24)

    email = prompt_email()
    password = prompt_password()

    db = SessionLocal()
    try:
        existing = db.execute(
            select(User).where(User.email == email).limit(1)
        ).scalar_one_or_none()

        if existing:
            raise SystemExit(f"User already exists: {email}")

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

        print()
        print(f"Admin created: {user.email} ({user.id})")
        print("Reminder: enable 2FA immediately after first login.")
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        raise SystemExit(130)
    finally:
        db.close()


if __name__ == "__main__":
    main()