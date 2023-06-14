from fastapi import FastAPI, Depends
from .hestia.api.api_v1.api import api_router
from .auth.users import current_active_user
from .auth.db import User
from .auth.auth_api import auth_router

app = FastAPI()

app.include_router(api_router)
app.include_router(auth_router)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
