import uuid
from fastapi.encoders import jsonable_encoder
from .base import CRUDBase
from sqlalchemy.orm import Session
from app.hestia.db.models import Station
from app.hestia.schemas.station import StationCreate, StationUpdate


class CRUDStation(CRUDBase[Station, StationCreate, StationUpdate]):
    def create_with_owner(
            self, db: Session, *, obj_in: StationCreate, owner_id: uuid.UUID
    ) -> Station:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
            self, db: Session, *, owner_id: uuid.UUID, skip: int = 0, limit: int = 100
    ):
        return (
            db.query(self.model)
            .filter(Station.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


station = CRUDStation(Station)
