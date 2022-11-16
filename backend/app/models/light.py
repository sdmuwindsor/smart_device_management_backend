from typing import TYPE_CHECKING
import enum
from sqlalchemy import Boolean, Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Lights(Base):
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    brightness = Column(Float)
    created = Column(DateTime)
    
    device_light  = relationship('Devices')