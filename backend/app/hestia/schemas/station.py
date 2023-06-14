from pydantic import BaseModel
from .device import DeviceData


class StationData(BaseModel):
    id: int
    devices: list[DeviceData]
