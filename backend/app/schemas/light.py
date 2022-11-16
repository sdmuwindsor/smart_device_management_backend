from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class LightBase(BaseModel):
    device_id: int
    brightness: float
    created: datetime
    name: str


class Light(LightBase):
    id: int

    class Config:
        orm_mode = True

