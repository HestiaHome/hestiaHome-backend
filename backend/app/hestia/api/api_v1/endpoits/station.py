from datetime import datetime

from fastapi import APIRouter, Response, Depends
from app.hestia.api.deps import get_db
from sqlalchemy.orm import Session
from app.hestia.db.models import Station, Device, User
from app.auth.users import super_user, current_active_user
from app.auth.db import User
from app.hestia.schemas.station import StationData
from .wsdata import manager

station_router = APIRouter()


@station_router.post("/create_station/", status_code=201)
def create_station(station_id: int,
                   name: str, response: Response,
                   db: Session = Depends(get_db),
                   user: User = Depends(super_user)):
    if db.query(Station).get(station_id):
        response.status_code = 400
        return {"detail": "SUBJECT ALREADY EXISTS"}
    station = Station(id=station_id, name=name)
    db.add(station)
    db.commit()
    return {"detail": "Subject create",
            "subject": {"id": station_id, "name": name}}


@station_router.post("/bind_station/")
def bind_station(station_id: int,
                 response: Response,
                 db: Session = Depends(get_db),
                 user: User = Depends(current_active_user)):
    station = db.query(Station).get(station_id)
    if not station:
        response.status_code = 400
        return {"detail": "STATION DOESN'T EXISTS"}
    station.user_id = user.id
    db.commit()
    return {"detail": f"Success add your station! Your id = {user.id}, "
                      f"station id = {station_id}."}


@station_router.get("/get_stations/")
def get_stations(db: Session = Depends(get_db), user: User = Depends(super_user)):
    stations = db.query(Station).all()
    return stations


@station_router.put("/send_data/{station_id}")
async def station_send_data(station_id: int,
                            data: StationData,
                            response: Response,
                            db: Session = Depends(get_db)):
    cur_station = db.query(Station).get(station_id)
    if not cur_station:
        response.status_code = 400
        return {"detail": "STATION DOESN'T EXIST"}
    data_to_user = dict()
    for device in data.devices:
        cur_device = db.query(Device).get(device.id)
        if not cur_device:
            response.status_code = 400
            return {"detail": f"DEVICE №{device.id} DOESN'T EXIST"}
        cur_device.data = device.data
        cur_device.status = device.status
        cur_time = datetime.now()
        cur_device.time = cur_time
        db.commit()
        data_to_user[device.id] = {"data": device.data,
                                   "status": device.status,
                                   "time": cur_time}
    if cur_station.user_id in manager.active_users.keys():
        websocket = manager.active_users[cur_station.user_id]
        await manager.send_json_message(data_to_user, websocket)
    return {"detail": "Success update devices."}
