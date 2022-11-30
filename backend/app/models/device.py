from typing import TYPE_CHECKING
import enum
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Category(enum.Enum):
    light = "Light"
    thermostat = "Thermostat"

class Devices(Base):
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    name = Column(String(50), index=True)
    category = Column(Enum(Category))
    power_rating = Column(Float)

    room_device = relationship('Rooms')