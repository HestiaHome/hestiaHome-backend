import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# from app.auth.db import User
from app.db.models import User

from fastapi import HTTPException
from app import schemas
from app import crud
from app.api import deps
from typing import List, Any

from app.core.log_settings import logger

router = APIRouter()


@router.get("/", response_model=List[schemas.Station])
def read_stations(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve stations"""
    logger.debug("Hello world!")
    if current_user.is_superuser:
        stations = crud.station.get_multi(db=db, skip=skip, limit=limit)
    else:
        stations = crud.station.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit)
    return stations


@router.post("/", response_model=schemas.Station, status_code=201)
def create_station(
        *,
        db: Session = Depends(deps.get_db),
        station_in: schemas.StationCreate,
        current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new station
    """
    station = crud.station.create_with_owner(
        db=db, obj_in=station_in, owner_id=current_user.id)
    return station


@router.put("/{id}", response_model=schemas.Station)
def update_station(
        *,
        db: Session = Depends(deps.get_db),
        id: uuid.UUID,
        station_in: schemas.StationUpdate,
        current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Update a station"""
    station = crud.station.get(db=db, id=id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    if not current_user.is_superuser and (station.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    station = crud.station.update(db=db, db_obj=station, odb_in=station_in)
    return station


@router.get("/{id}", response_model=schemas.Station)
def get_station(
        *,
        db: Session = Depends(deps.get_db),
        id: uuid.UUID,
        current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get station by ID
    """

    station = crud.station.get(db=db, id=id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    if not current_user.is_superuser and (station.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return station


@router.delete("/{id}", response_model=schemas.Station)
def delete_station(
        *,
        db: Session = Depends(deps.get_db),
        id: uuid.UUID,
        current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Remove station
    """
    station = crud.station.get(db=db, id=id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    if not current_user.is_superuser and (station.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    station = crud.station.remove(db=db, id=id)
    return station


# TODO: Разобраться и переделать метод отправки данных с умной станции
# @router.put("/send_data/{station_id}")
# async def station_send_data(station_id: uuid.UUID,
#                             data: StationData,
#                             response: Response,
#                             db: Session = Depends(deps.get_db)):
#     cur_station = db.query(Station).get(station_id)
#     if not cur_station:
#         raise HTTPException(status_code=404, detail="Station not found")
#     data_to_user = dict()
#     for device in data.devices:
#         cur_device = db.query(Device).get(device.id)
#         if not cur_device:
#             response.status_code = 400
#             return {"detail": f"DEVICE №{device.id} DOESN'T EXIST"}
#         cur_device.data = device.data
#         cur_device.status = device.status
#         cur_time = datetime.now()
#         cur_device.time = cur_time
#         db.commit()
#         data_to_user[device.id] = {"data": device.data,
#                                    "status": device.status,
#                                    "time": cur_time}
#     if cur_station.user_id in manager.active_users.keys():
#         websocket = manager.active_users[cur_station.user_id]
#         await manager.send_json_message(data_to_user, websocket)
#     return {"detail": "Success update devices."}
