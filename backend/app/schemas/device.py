from typing import Optional

from pydantic import BaseModel
from app.models.device import Category


# Shared properties
class DeviceBase(BaseModel):
    room_id: int
    name: str
    category: Category 



# Properties to receive via API on creation
class DeviceCreate(DeviceBase):
    pass


# Properties to receive via API on update
class DeviceUpdate(DeviceBase):
    pass
    

class Device(DeviceBase):
    id: int

    class Config:
        orm_mode = True

