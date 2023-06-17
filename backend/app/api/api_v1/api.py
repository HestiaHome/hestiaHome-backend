from fastapi import APIRouter

from .endpoits import devices, stations, wsdata, users, login

api_router = APIRouter()

api_router.include_router(
    login.router,
    tags=["login"])
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)
api_router.include_router(
    stations.router,
    prefix="/station",
    tags=["station"]
)
api_router.include_router(
    devices.router,
    prefix="/devices",
    tags=["devices"]
)
api_router.include_router(
    wsdata.router,
    # prefix="/ws",
    tags=["websockets"]
)
