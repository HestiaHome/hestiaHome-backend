import uuid
from typing import Optional
from pydantic import BaseModel


# Shared properties
class DeviceBase(BaseModel):
    name: Optional[str] = None
    data: Optional[str] = None
    type: Optional[int] = None
    command: Optional[str] = None
    status: Optional[bool] = None


class DeviceCreate(DeviceBase):
    name: str


class DeviceUpdate(DeviceBase):
    pass


# Properties shared by models stored in DB
class DeviceInDBBase(DeviceBase):
    id: uuid.UUID
    name: str
    data: str
    command: str
    status: bool
    room_id: int
    station_id: uuid.UUID

    class Config:
        orm_mode = True


# Properties to return to client
class Device(DeviceInDBBase):
    pass


class DeviceData(BaseModel):
    id: uuid.UUID
    # device_type: int
    data: str
    status: bool
