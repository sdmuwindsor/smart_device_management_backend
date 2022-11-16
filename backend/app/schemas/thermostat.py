from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Shared propertie
class ThermostatBase(BaseModel):
    device_id: int
    humidity: float
    inside_temperature: float
    outside_temperature: float
    created: datetime
    name: str


class Thermostat(ThermostatBase):
    id: int

    class Config:
        orm_mode = True

