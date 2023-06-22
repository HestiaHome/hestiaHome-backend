from typing import Generator, Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db.models import metadata
from app.core.config import settings
from app.main import app
from app.api import deps
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers

from app.core.log_settings import logger

# TODO: Автоматизировать создание test_db через фикстуру


DATABASE_URL_TEST = f"postgresql://" \
                    f"{settings.POSTGRES_USER}:{settings.POSTGRES_PASS}" \
                    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/" \
                    f"test_db"

engine_test = create_engine(DATABASE_URL_TEST)
SessionLocal = sessionmaker(engine_test, expire_on_commit=False)
metadata.bind = engine_test


def override_get_db() -> Generator:
    with SessionLocal() as session:
        yield session


app.dependency_overrides[deps.get_db] = override_get_db


@pytest.fixture(autouse=True, scope='session')
def prepare_database(db):
    metadata.create_all(engine_test)
    yield
    db.close()
    metadata.drop_all(engine_test)


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def superuser_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return get_superuser_token_headers(client, db)


@pytest.fixture(scope="session")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
