import uuid
from pydantic import BaseModel
from .device import DeviceData


class StationData(BaseModel):
    id: uuid.UUID
    devices: list[DeviceData]
