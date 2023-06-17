import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# from app.hestia.api.deps import get_db

# from app.auth.db import User
from app.db.models import User
from app import schemas
from app import crud
from app.api import deps

from typing import List, Any

router = APIRouter()


# TODO: понять нужно ли в данный endpoint передавать station_id
@router.get("/", response_model=List[schemas.Device])
def read_devices(
        *,
        station_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve devices by station id
    :param station_id:
    :param skip:
    :param limit:
    :param db:
    :param current_user:
    :return:
    """
    devices = []
    station = crud.station.get(db=db, id=station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    if current_user.is_superuser:
        devices = crud.device.get_multi_by_station(
            db=db, skip=skip, limit=limit, station_id=station_id
        )
    else:
        if station.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="This user hasn't this station")
        else:
            devices = crud.device.get_multi_by_station(
                db=db, skip=skip, limit=limit, station_id=station_id
            )
    return devices


@router.post("/", response_model=schemas.Device)
def create_device(
        *,
        station_id: uuid.UUID,
        device_in: schemas.DeviceCreate,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new device by station id
    :param station_id:
    :param device_in:
    :param db:
    :param current_user:
    :return:
    """
    station = crud.station.get(db=db, id=station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    if current_user.is_superuser:
        device = crud.device.create_with_station(
            db=db, obj_in=device_in, station_id=station_id
        )
    else:
        if station.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="This user hasn't this station")
        else:
            device = crud.device.create_with_station(
                db=db, obj_in=device_in, station_id=station_id
            )
    return device


@router.put("/{id}", response_model=schemas.Device)
def update_device(
        *,
        db: Session = Depends(deps.get_db),
        id: uuid.UUID,
        device_in: schemas.DeviceUpdate,
        current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Update a device
    :param db:
    :param id:
    :param device_in:
    :param current_user:
    :return:
    """
    device = crud.device.get(db=db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    stations = crud.station.get_multi_by_owner(db=db, owner_id=current_user.id)
    stations_id = [station.id for station in stations]
    if not current_user.is_superuser and device.station_id not in stations_id:
        raise HTTPException(status_code=400, detail="Not enough permission")
    device = crud.device.update(db=db, db_obj=device, obj_in=device_in)
    return device


@router.get("/{id}", response_model=schemas.Device)
def get_device(
        *,
        id: uuid.UUID,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    device = crud.device.get(db=db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    stations = crud.station.get_multi_by_owner(db=db, owner_id=current_user.id)
    stations_id = [station.id for station in stations]
    if not current_user.is_superuser and device.station_id not in stations_id:
        raise HTTPException(status_code=400, detail="Not enough permission")
    return device


@router.delete("/{id}", response_model=schemas.Device)
def delete_device(
        *,
        id: uuid.UUID,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    device = crud.device.get(db=db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    stations = crud.station.get_multi_by_owner(db=db, owner_id=current_user.id)
    stations_id = [station.id for station in stations]
    if not current_user.is_superuser and device.station_id not in stations_id:
        raise HTTPException(status_code=400, detail="Not enough permission")
    device = crud.device.remove(db=db, id=id)
    return device
