# Hestia Home
Backend part of the application Hestia Home 
## Tools
- Python 3.10
- FastAPI
- SQLAlchemy 1.4.46 
- Alembic
- Docker/docker-compose
- PostgreSQL
- PgAdmin

## Quick start:

### 1. clone this project
### 2. create .env
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=main_db
DB_USER=root
DB_PASS=root
```
### 3. Install requirements in venv.
#### On Linux 
`(venv) pip install -r requirements.txt`

#### On Windows. 
In `requiremets.txt` change *psycopg2-binary* on *psycorg2*

`(venv) pip install -r requirements.txt`

### 4. Start app


`uvicorn app.main:app --reload`

### 5. Start docker compose

`docker compose up`

### 6. Make migrations

```
alembic revision --message="Initial" --autogenerate
alembic upgrade head
```

### 7. Check tests.
You should create "test_db" in PgAdmin4 and then:
`pytest tests/`
