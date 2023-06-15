import uuid
from typing import Optional
from pydantic import BaseModel
from .device import DeviceData


# Shared properties
class StationBase(BaseModel):
    name: Optional[str] = None


# Properties to receive on item creation
class StationCreate(StationBase):
    pass


# Properties to receive on item update
class StationUpdate(StationBase):
    pass


# Properties shared by models stored in DB
class StationInDBBase(StationBase):
    id: uuid.UUID
    name: str
    owner_id: uuid.UUID

    class Config:
        orm_mode = True


# Properties to return to client
class Station(StationInDBBase):
    pass


class StationData(BaseModel):
    id: uuid.UUID
    devices: list[DeviceData]
