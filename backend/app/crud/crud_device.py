import uuid
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.db.models import Device
from app.schemas.device import DeviceCreate, DeviceUpdate
from .base import CRUDBase


class CRUDDevice(CRUDBase[Device, DeviceCreate, DeviceUpdate]):

    def create_with_station(
            self, db: Session, obj_in: DeviceCreate, station_id: uuid.UUID
    ) -> Device:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, station_id=station_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_station(
            self, db: Session, station_id: uuid.UUID, skip: int = 0, limit: int = 100
    ):
        return (
            db.query(self.model)
            .filter(Device.station_id == station_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


device = CRUDDevice(Device)
