from fastapi import FastAPI, Depends

from .auth.db import User
from .auth.schemas import UserCreate, UserRead, UserUpdate
from .auth.users import auth_backend, current_active_user, fastapi_users
from .routers.wsdata import ws_router
from .routers.station import station_router
from app.routers.devices_data import router_device

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    ws_router,
    # prefix="/ws",
    tags=["websockets"]
)
# app.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/auth",
#     tags=["auth"],
# )
# app.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/auth",
#     tags=["auth"],
# )
app.include_router(
    station_router,
    prefix="/station",
    tags=["station"]
)
app.include_router(
    router_device,
    prefix="/devices",
    tags=["devices"]
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
