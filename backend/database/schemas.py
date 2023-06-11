from pydantic import BaseModel


class DeviceCreate(BaseModel):
    id: int
    name: str
    type: str


class DeviceData(BaseModel):
    # id: int
    value: str
    # type: int
