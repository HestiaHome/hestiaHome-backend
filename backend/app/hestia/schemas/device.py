import uuid
from pydantic import BaseModel


class DeviceData(BaseModel):
    id: uuid.UUID
    # device_type: int
    data: str
    status: bool
