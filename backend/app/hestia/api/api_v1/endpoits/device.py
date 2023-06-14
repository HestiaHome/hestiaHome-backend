from datetime import datetime

from fastapi import APIRouter, Response, Depends
from sqlalchemy.orm import Session

from app.hestia.api.deps import get_db
from app.hestia.db.models import Device
from app.hestia.schemas.device import DeviceData

from app.core.log_settings import logger

device_router = APIRouter()


@device_router.put("/send_data/{device_id}")
def update_data_from_devices(device_id: int,
                             response: Response, data: DeviceData, db: Session = Depends(get_db)):
    device = Device
    cur_device = db.query(device).get(device_id)
    if not cur_device:
        response.status_code = 400
        return {"message": "device doesn't exist"}
    cur_device.data = data.value
    time_now = datetime.now()
    cur_device.time = time_now
    db.commit()
    logger.debug(f"Device №{device_id} get new value: {data.value}")
    return {"message": "success update",
            "device_id": device_id,
            "value": data.value, "time": time_now}
