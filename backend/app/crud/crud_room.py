from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Rooms
from app.schemas.room import Room, RoomBase, RoomCreate, RoomUpdate


class CRUDRoom(CRUDBase[Rooms, RoomCreate, RoomUpdate]):
    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[Rooms]:
        return db.query(Rooms).filter(Rooms.user_id == user_id).all()
    
    def get(self, db: Session, *, id: int) -> Optional[Rooms]:
        return db.query(Rooms).filter(Rooms.id == id).first()

    def create(self, db: Session, *, obj_in: RoomCreate) -> Rooms:
        db_obj = Rooms(
            user_id=obj_in.user_id,
            name=obj_in.name
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, obj_in: RoomCreate, id: int) -> Rooms:
        db_room = self.get(db, id=id)
        db_room.user_id = obj_in.user_id
        db_room.name = obj_in.name
        db.commit()
        db.refresh(db_room)

        return db_room


room = CRUDRoom(Rooms)
