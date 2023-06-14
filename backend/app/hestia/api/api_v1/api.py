from fastapi import APIRouter

from .endpoits import device, station, wsdata

api_router = APIRouter()

api_router.include_router(
    wsdata.ws_router,
    # prefix="/ws",
    tags=["websockets"]
)

api_router.include_router(
    station.station_router,
    prefix="/station",
    tags=["station"]
)
api_router.include_router(
    device.device_router,
    prefix="/devices",
    tags=["devices"]
)
