from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

SQLALCHEMY_DB_URL = f"postgresql://" \
                    f"{settings.POSTGRES_USER}:{settings.POSTGRES_PASS}" \
                    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/" \
                    f"{settings.POSTGRES_DB_NAME}"
engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
