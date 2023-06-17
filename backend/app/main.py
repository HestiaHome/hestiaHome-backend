from fastapi import FastAPI, Depends
from app.api.api_v1.api import api_router
from app.api.deps import get_current_active_user
from app.db.models import User
# from .auth.auth_api import auth_router

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)
# app.include_router(auth_router)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(get_current_active_user)):
    return {"message": f"Hello {user.email}!"}
