from typing import Any, Dict, Optional, Union
import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import Users
from app.schemas.user import UserCreate, UserUpdate
from app.utils.mail import send_mails
from app.models import Devices, Rooms
from app import crud

class CRUDUser(CRUDBase[Users, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Users]:
        return db.query(Users).filter(Users.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> Users:
        db_obj = Users(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        send_mails.send_confirmation_mail(obj_in.first_name,obj_in.email)
        return db_obj

    def authenticate(
        self,
        db: Session,
        *,
        email: str,
        password: str
    ):
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def get_power_consumption_by_dates(self, db: Session, *, start_date: datetime, end_date: datetime, user_id: int) -> Optional[Users]:
        device = db.query(Devices).join(
            Rooms,
            Rooms.id == Devices.room_id
        ).filter(
            Rooms.user_id == user_id,
        ).all()
        final_df = pd.DataFrame()
        for i in device:
            if i.__dict__['category'].value =='Light':
                power = crud.light.get_power_consumption_by_dates(db, start_date=start_date, end_date=end_date, device_id=i.__dict__['id'])
            else :
                power = crud.thermostat.get_power_consumption_by_dates(db, start_date=start_date, end_date=end_date, device_id=i.__dict__['id'])
            df = pd.DataFrame.from_records(power)
            final_df = pd.concat([final_df,df],ignore_index=True)
        if len(final_df) < 1:
            return {}
        final_df = final_df.groupby('date').agg({'power_consumption':'sum'}).reset_index()
        return final_df.to_dict('records')


user = CRUDUser(Users)


