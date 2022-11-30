from typing import Any, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Thermostats
from app.schemas.thermostat import Thermostat, ThermostatBase, ThermostatCreate, ThermostatUpdate


class CRUDThermostat(CRUDBase[Thermostats, ThermostatCreate, ThermostatUpdate]):
    def get_temperature_by_dates(self, db: Session, *, start_date: datetime, end_date: datetime, device_id: int, type: str) -> Optional[Thermostats]:
        return db.query(Thermostats).filter(Thermostats.created.between(start_date, end_date)).all()

    def get_humidity_by_dates(self, db: Session, *, start_date: datetime, end_date: datetime, device_id: int) -> Optional[Thermostats]:
        return db.query(Thermostats).filter(Thermostats.created.between(start_date, end_date)).all()

    def get_power_consumption_by_dates(self, db: Session, *, start_date: datetime, end_date: datetime, device_id: int) -> Optional[Thermostats]:
        return db.query(Thermostats).filter(Thermostats.created.between(start_date, end_date)).all()

thermostat = CRUDThermostat(Thermostats)
