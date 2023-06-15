from typing import Generator
from ..db.session import SessionLocal
from app.auth.users import current_active_user


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
