import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app import crud
from app.db import models
from app.schemas.station import StationCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_station(db: Session, *, owner_id: Optional[uuid.UUID] = None) -> models.Station:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    name = random_lower_string()
    station_in = StationCreate(name=name)
    return crud.station.create_with_owner(db=db, obj_in=station_in, owner_id=owner_id)
