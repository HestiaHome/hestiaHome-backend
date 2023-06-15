from fastapi import APIRouter

from .endpoits import devices, stations, wsdata

api_router = APIRouter()

api_router.include_router(
    wsdata.router,
    # prefix="/ws",
    tags=["websockets"]
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
