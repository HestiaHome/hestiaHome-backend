from sqlalchemy.orm import Session

from app import crud
from app.schemas.station import StationCreate, StationUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_item(db: Session) -> None:
    name = random_lower_string()
    station_in = StationCreate(name=name)
    user = create_random_user(db)
    station = crud.station.create_with_owner(db=db, obj_in=station_in, owner_id=user.id)
    assert station.name == name
    assert station.owner_id == user.id


def test_get_item(db: Session) -> None:
    name = random_lower_string()
    station_in = StationCreate(name=name)
    user = create_random_user(db)
    station = crud.station.create_with_owner(db=db, obj_in=station_in, owner_id=user.id)
    stored_station = crud.station.get(db=db, id=station.id)
    assert stored_station
    assert station.id == stored_station.id
    assert station.name == stored_station.name
    assert station.owner_id == stored_station.owner_id


def test_update_station(db: Session) -> None:
    name = random_lower_string()
    station_id = StationCreate(name=name)
    user = create_random_user(db)
    station = crud.station.create_with_owner(db=db, obj_in=station_id, owner_id=user.id)
    name2 = random_lower_string()
    station_update = StationUpdate(name=name2)
    station2 = crud.station.update(db=db, db_obj=station, obj_in=station_update)
    assert station.id == station2.id
    assert name2 == station2.name
    assert station.owner_id == station2.owner_id


def test_delete_item(db: Session) -> None:
    name = random_lower_string()
    station_in = StationCreate(name=name)
    user = create_random_user(db)
    station = crud.station.create_with_owner(db=db, obj_in=station_in, owner_id=user.id)
    station2 = crud.station.remove(db=db, id=station.id)
    station3 = crud.station.get(db=db, id=station.id)
    assert station3 is None
    assert station2.id == station.id
    assert station2.name == station.name
    assert station2.owner_id == user.id
