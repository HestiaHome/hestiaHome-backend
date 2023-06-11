#!/bin/bash

alembic revision --autogenerate -m "Database creation"
alembic upgrade head

gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
