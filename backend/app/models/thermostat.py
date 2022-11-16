from typing import TYPE_CHECKING
import enum
from sqlalchemy import Boolean, Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Thermostats(Base):
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    inside_temperature = Column(Float)
    outside_temperature = Column(Float)
    humidity= Column(Float)
    created = Column(DateTime)
    
    device_light  = relationship('Devices')