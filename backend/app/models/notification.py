from typing import TYPE_CHECKING
import enum
from sqlalchemy import Boolean, Column, Integer, DateTime, ForeignKey, Float, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Notifications(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String(50), index=True)
    title = Column(String(50), index=True)
    
    user_notification  = relationship('Users')