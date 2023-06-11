from datetime import datetime

from fastapi import APIRouter, Response, Depends
from database.database import SessionLocal
from database.models import Station, Device, User
# from database.models import User as User_BD
# from database.schemas import DeviceCreate
from ..auth.users import super_user, current_active_user
from ..auth.db import User
from .schemas import StationData
from .wsdata import manager

station_router = APIRouter()

session = SessionLocal()


@station_router.post("/create_station/", status_code=201)
def create_station(station_id: int, name: str, response: Response, user: User = Depends(super_user)):
    if session.query(Station).get(station_id):
        response.status_code = 400
        return {"detail": "SUBJECT ALREADY EXISTS"}
    station = Station(id=station_id, name=name)
    session.add(station)
    session.commit()
    return {"detail": "Subject create", "subject": {"id": station_id, "name": name}}


@station_router.post("/bind_station/")
def bind_station(station_id: int, response: Response, user: User = Depends(current_active_user)):
    station = session.query(Station).get(station_id)
    if not station:
        response.status_code = 400
        return {"detail": "STATION DOESN'T EXISTS"}
    station.user_id = user.id
    session.commit()
    return {"detail": f"Success add your station! Your id = {user.id}, station id = {station_id}."}


@station_router.get("/get_stations/")
def get_stations(user: User = Depends(super_user)):
    stations = session.query(Station).all()
    return stations


@station_router.put("/send_data/{station_id}")
async def station_send_data(station_id: int, data: StationData, response: Response):
    cur_station = session.query(Station).get(station_id)
    if not cur_station:
        response.status_code = 400
        return {"detail": "STATION DOESN'T EXIST"}
    data_to_user = dict()
    for device in data.devices:
        cur_device = session.query(Device).get(device.id)
        if not cur_device:
            response.status_code = 400
            return {"detail": f"DEVICE №{device.id} DOESN'T EXIST"}
        cur_device.data = device.data
        cur_device.status = device.status
        cur_time = datetime.now()
        cur_device.time = cur_time
        session.commit()
        data_to_user[device.id] = {"data": device.data, "status": device.status, "time": cur_time}
    if cur_station.user_id in manager.active_users.keys():
        websocket = manager.active_users[cur_station.user_id]
        await manager.send_json_message(data_to_user, websocket)
    return {"detail": "Success update devices."}

# @station_router.post("/link_sensor/{sensor_id}", status_code=200)
# def link_sensor_to_device(response: Response, sensor_id: int, sensor: SensorCreate, user: User = Depends(super_user)):
#     if sensor.type not in sensor_types:
#         response.status_code = 400
#         return {"detail": "INVALID TYPE"}
#     sensor = sensor_types[sensor.type](id=sensor.id, name=sensor.name, device_id=sensor_id)
#     session.add(sensor)
#     session.commit()
#     return {"detail": "success", "sensor": sensor}
