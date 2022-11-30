from typing import Any, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Lights, Devices
from app.schemas.light import Light, LightBase, LightCreate, LightUpdate


class CRUDLight(CRUDBase[Lights, LightCreate, LightUpdate]):
    def get_brightness_by_dates(self, db: Session, *, start_date: datetime, end_date: datetime, device_id: int) -> Optional[Lights]:
        return db.query(Lights).filter(Lights.created.between(start_date, end_date),Lights.device_id==device_id).all()

    def get_power_consumption_by_dates(self, db: Session, *, start_date: datetime, end_date: datetime, device_id: int) -> Optional[Lights]:
        data = db.query(Lights).filter(Lights.created.between(start_date, end_date),Lights.device_id==device_id).all()
        df = pd.DataFrame.from_records(data)
        df = df.sort_values(by=Lights.created, ascending=False).reset_index(drop=True)
        df['date'] = df[Lights.brightness].apply(lambda x: str(x).split(' ')[0])
        df[Lights.brightness] = df[Lights.brightness].apply(lambda x: 1 if x>0 else 0)
        df['next_time'] = df[Lights.created].shift(-1)
        df['power_consumption'] = df.next_time - df[Lights.created] / pd.Timedelta(hours=1)
        df = df[df[Lights.brightness]==1]
        df = df.groupby("date").agg({'power_consumption':'sum'})
        power_data = db.query(Devices.power_rating).filter(Devices.id==device_id).first()
        df['power_consumption'] = df['power_consumption']*power_data['power_rating']
        return df.to_dict('records')

light = CRUDLight(Lights)
