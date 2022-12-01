from typing import Any, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
import pandas as pd
from app.crud.base import CRUDBase
from app.models import Thermostats, Devices
from app.schemas.thermostat import Thermostat, ThermostatBase, ThermostatCreate, ThermostatUpdate


class CRUDThermostat(CRUDBase[Thermostats, ThermostatCreate, ThermostatUpdate]):
    def get_temperature_by_dates(self, db: Session, *, start_date: datetime, end_date: datetime, device_id: int, type: str) -> Optional[Thermostats]:
        data =  db.query(Thermostats).filter(Thermostats.created.between(start_date, end_date),Thermostats.device_id==device_id).all()
        data = [i.__dict__ for i in data]
        df = pd.DataFrame.from_records(data)
        if 'inside' in type:
            df = df[['created','inside_temperature']]
            df['created'] = df['created'].apply(lambda x: str(x).split(' ')[0])
            df = df.groupby('created').agg({'inside_temperature':np.mean}).reset_index()
        else:
            df = df[['created','outside_temperature']]
            df['created'] = df['created'].apply(lambda x: str(x).split(' ')[0])
            df = df.groupby('created').agg({'outside_temperature':np.mean}).reset_index()
        return df.to_dict('records')

    def get_humidity_by_dates(self, db: Session, *, start_date: datetime, end_date: datetime, device_id: int) -> Optional[Thermostats]:
        data =  db.query(Thermostats).filter(Thermostats.created.between(start_date, end_date),Thermostats.device_id==device_id).all()
        data = [i.__dict__ for i in data]
        df = pd.DataFrame.from_records(data)
        df = df[['created','humidity']]
        df['created'] = df['created'].apply(lambda x: str(x).split(' ')[0])
        df = df.groupby('created').agg({'humidity':np.mean}).reset_index()
        return df.to_dict('records')

    def get_power_consumption_by_dates(self, db: Session, *, start_date: datetime, end_date: datetime, device_id: int) -> Optional[Thermostats]:
        data = db.query(Thermostats).filter(Thermostats.created.between(start_date, end_date),Thermostats.device_id==device_id).all()
        data = [i.__dict__ for i in data]
        df = pd.DataFrame.from_records(data)
        df = df[['created','inside_temperature']]
        df = df.groupby('created').agg({'inside_temperature':'count'}).reset_index()
        df.rename(columns={'inside_temperature':'power_consumption'},inplace=True)
        df['power_consumption'] = df['power_consumption'].apply(lambda x: x*24/150)
        power_data = db.query(Devices.power_rating).filter(Devices.id==device_id).first()
        df['power_consumption'] = df['power_consumption']*(power_data[0]+power_data[0]*random.uniform(-0.1,0.1))
        return df.to_dict('records')

thermostat = CRUDThermostat(Thermostats)
