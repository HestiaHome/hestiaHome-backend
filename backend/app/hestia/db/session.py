from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DB_PASS, DB_HOST, DB_PORT, DB_NAME, DB_USER

db_name = "postgresql"

SQLALCHEMY_DB_URL = f"{db_name}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
