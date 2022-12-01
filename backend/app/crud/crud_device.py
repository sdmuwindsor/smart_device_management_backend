from typing import Any, Dict, Optional

from sqlalchemy.orm import Session
from datetime import datetime
from app.crud.base import CRUDBase
from app import crud
from app.models import Devices, Rooms
from app.schemas.device import Device, DeviceBase, DeviceCreate, DeviceUpdate
from app.mqtt.mqtt_control import mqtt_control

class CRUDDevice(CRUDBase[Devices, DeviceCreate, DeviceUpdate]):
    def get_by_room_id(self, db: Session, *, room_id: int) -> Optional[Devices]:
        return db.query(Devices).filter(Devices.room_id == room_id).all()
    
    def get(self, db: Session, *, id: int, start_date: datetime, end_date: datetime) -> Optional[Devices]:
        device_details = db.query(Devices).filter(Devices.id == id).first()
        print(device_details.__dict__['category'].value,device_details.__dict__)
        if device_details.__dict__['category'].value == 'Light':
            brightness = crud.light.get_brightness_by_dates(db, start_date=start_date, end_date=end_date, device_id=id)
            power = crud.light.get_power_consumption_by_dates(db, start_date=start_date, end_date=end_date, device_id=id)
            out = {'details':device_details,'brightness':brightness,'power_consumption':power}
        elif device_details.__dict__['category'].value == 'Thermostat':
            inside_temperature = crud.thermostat.get_temperature_by_dates(db, start_date=start_date, end_date=end_date, device_id=id, type="inside")
            ouside_temperature = crud.thermostat.get_temperature_by_dates(db, start_date=start_date, end_date=end_date, device_id=id, type="outside")
            humidity = crud.thermostat.get_humidity_by_dates(db, start_date=start_date, end_date=end_date, device_id=id)
            power = crud.thermostat.get_power_consumption_by_dates(db, start_date=start_date, end_date=end_date, device_id=id)
            out = {'details':device_details,'inside_temperature':inside_temperature,"ouside_temperature":ouside_temperature,"humidity":humidity,'power_consumption':power}
        return out

    def create(self, db: Session, *, obj_in: DeviceCreate) -> Devices:
        db_obj = Devices(
            room_id=obj_in.room_id,
            name=obj_in.name,
            category=obj_in.category,
            power_rating=obj_in.power_rating
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        mqtt_control.add_a_device(str(db_obj.id),db_obj.category)
        return db_obj

    def update(self, db: Session, *, obj_in: DeviceCreate, id: int) -> Devices:
        db_device = self.get(db, id=id)
        db_device.room_id = obj_in.room_id
        db_device.name = obj_in.name
        db_device.category = obj_in.category
        db_device.power_rating = obj_in.power_rating
        db.commit()
        db.refresh(db_device)

        return db_device

    def get_by_category(self, category_name, user_id, db:Session):
        return db.query(Devices).join(
            Rooms,
            Rooms.id == Devices.room_id
        ).filter(
            Rooms.user_id == user_id,
            Devices.category == category_name
        ).all()

device = CRUDDevice(Devices)
