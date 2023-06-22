import random
import string
from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings

from app.crud import user
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from app.db.session import SessionLocal


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=12))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_superuser_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    obj_in = UserCreate(username=settings.FIRST_SUPERUSER_USERNAME,
                        email=settings.FIRST_SUPERUSER_EMAIL,
                        password=settings.FIRST_SUPERUSER_PASSWORD, is_superuser=True)
    superuser = user.create(db=db, obj_in=obj_in)
    login_data = {
        "username": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
