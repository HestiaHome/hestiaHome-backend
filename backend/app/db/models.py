import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID


# TODO: Возможно стоит переделать Категории и Room в класс enum.Enum
# TODO: Переписать классы под SQLAlchemy 2.0

class Base(DeclarativeBase):
    pass


metadata = Base.metadata


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False)
    username = Column(String(30), nullable=False)
    create_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    user_type = Column(Integer, ForeignKey("user_category.id"))

    user_category = relationship("UserCategory", back_populates="users")
    stations = relationship("Station", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r})"


class UserCategory(Base):
    __tablename__ = "user_category"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    users = relationship("User", back_populates="user_category")

    def __repr__(self):
        return f"User Category: id={self.id!r}, name={self.name!r}"


class Station(Base):
    __tablename__ = "station"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(30), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)

    user = relationship("User", back_populates="stations")
    devices = relationship("Device", back_populates="station")

    def __repr__(self):
        return f"Station: id={self.id!r}, name={self.name!r}, user_id={self.owner_id!r}"


class Room(Base):
    __tablename__ = "room"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(30))

    devices = relationship("Device", back_populates="room")


class Device(Base):
    __tablename__ = "device"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(30), nullable=False)
    room_id = Column(UUID(as_uuid=True), ForeignKey("room.id"))
    type = Column(Integer, ForeignKey("device_type.id"))
    data = Column(String)
    command = Column(String)
    time = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(Boolean, default=False)
    station_id = Column(UUID(as_uuid=True), ForeignKey("station.id"))

    device_type = relationship("DeviceType", back_populates="devices")
    station = relationship("Station", back_populates="devices")
    room = relationship("Room", back_populates="devices")

    def __repr__(self):
        return f"Device: name={self.name!r}, time={self.time!r}, status={self.status!r}"


class DeviceType(Base):
    __tablename__ = "device_type"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    devices = relationship("Device", back_populates="device_type")

    def __repr__(self):
        return f"Device Type: id={self.id!r}, name={self.name!r}"
