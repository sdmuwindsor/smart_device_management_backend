from typing import Any, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
import numpy as np
import random
from app.crud.base import CRUDBase
from app.models import Lights, Devices
from app.schemas.light import Light, LightBase, LightCreate, LightUpdate
import pandas as pd

class CRUDLight(CRUDBase[Lights, LightCreate, LightUpdate]):
    def get_brightness_by_dates(self, db: Session, *, start_date: datetime, end_date: datetime, device_id: int) -> Optional[Lights]:
        data = db.query(Lights).filter(Lights.created.between(start_date, end_date),Lights.device_id==device_id,Lights.brightness!=0).all()
        data = [i.__dict__ for i in data]
        df = pd.DataFrame.from_records(data)
        df = df[['created','brightness']]
        df['created'] = df['created'].apply(lambda x: str(x).split(' ')[0])
        df = df.groupby('created').agg({'brightness':np.mean}).reset_index()
        return df.to_dict('records')

    def get_power_consumption_by_dates(self, db: Session, *, start_date: datetime, end_date: datetime, device_id: int) -> Optional[Lights]:
        data = db.query(Lights).filter(Lights.created.between(start_date, end_date),Lights.device_id==device_id).all()
        data = [i.__dict__ for i in data]
        df = pd.DataFrame.from_records(data)
        df = df.sort_values(by='created', ascending=False).reset_index(drop=True)
        df['date'] = df['created'].apply(lambda x: str(x).split(' ')[0])
        df['brightness'] = df['brightness'].apply(lambda x: 1 if x>0 else 0)
        df['next_time'] = df['created'].shift(-1)
        df['power_consumption'] = abs(df.next_time - df['created']) / pd.Timedelta(hours=1)
        print(df)
        df = df[df['brightness']==1]
        df = df.groupby("date").agg({'power_consumption':'sum'}).reset_index()
        print(df)
        power_data = db.query(Devices.power_rating).filter(Devices.id==device_id).first()
        df['power_consumption'] = df['power_consumption']*(power_data[0]+power_data[0]*random.uniform(-0.1,0.1))
        return df.to_dict('records')

light = CRUDLight(Lights)
