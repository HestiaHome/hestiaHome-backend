import asyncio

from log_settings import logger
from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from database.database import SessionLocal
from database.models import User

ws_router = APIRouter()

session = SessionLocal()


class ConnectionManager:

    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.active_users = dict()

    def write_active_user(self, websocket: WebSocket, user_id: int):
        self.active_users[user_id] = websocket

    def remove_active_user(self, user_id: int):
        self.active_users.pop(user_id)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_personal_message(message: str, websocket: WebSocket):
        await websocket.send_text(message)

    @staticmethod
    async def send_json_message(data: dict, websocket: WebSocket):
        await websocket.send_json(data)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@ws_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    cur_user = session.query(User).get(client_id)
    if not cur_user:
        logger.debug(f"User {client_id} can't connect to websocket, because user doesn't exist")
        await manager.send_personal_message(f"User-{client_id} doesn't exist.", websocket)
    else:
        logger.debug(f"User {client_id} has connect to websocket")
        manager.write_active_user(websocket, client_id)
        logger.debug(f"Current active users: {manager.active_users.keys()} after connecting user #{client_id}")
        try:
            while True:
                data = await websocket.receive_text()
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            manager.remove_active_user(client_id)
            logger.debug(f"User {client_id} has disconnect to websocket")
            logger.debug(f"Current active users: {manager.active_users.keys()} after disconnecting user #{client_id}")
