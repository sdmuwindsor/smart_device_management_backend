from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Devices, Rooms
from app.schemas.device import Device, DeviceBase, DeviceCreate, DeviceUpdate
from app.mqtt.mqtt_control import mqtt_control


from app.simulation import LightSim, ThermostatSim
light_sim_obj = LightSim.LightSimulation()
themostat_sim_obj = ThermostatSim.ThermostatSimulation()


class CRUDDevice(CRUDBase[Devices, DeviceCreate, DeviceUpdate]):
    def get_by_room_id(self, db: Session, *, room_id: int) -> Optional[Devices]:
        return db.query(Devices).filter(Devices.room_id == room_id).all()
    
    def get(self, db: Session, *, id: int) -> Optional[Devices]:
        # print(os.listdir())
        return db.query(Devices).filter(Devices.id == id).first()

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
        mqtt_control.add_a_device(str(db_obj.id),db_obj.category.value)
        light_sim_obj.generate_synthetic_data(db_obj.id)
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
