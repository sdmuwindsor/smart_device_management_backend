from typing import Optional

from pydantic import BaseModel


# Shared properties
class RoomBase(BaseModel):
    user_id: int
    name: str


# Properties to receive via API on creation
class RoomCreate(RoomBase):
    pass


# Properties to receive via API on update
class RoomUpdate(RoomBase):
    pass
    

class Room(RoomBase):
    id: int

    class Config:
        orm_mode = True

