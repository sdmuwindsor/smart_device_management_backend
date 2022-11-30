from typing import Any, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Lights
from app.schemas.light import Light, LightBase, LightCreate, LightUpdate


class CRUDLight(CRUDBase[Lights, LightCreate, LightUpdate]):
    def get_by_dates(self, db: Session, *, start_date: datetime, end_date: datetime) -> Optional[Lights]:
        return db.query(Lights).filter(Lights.created.between(start_date, end_date)).all()

light = CRUDLight(Lights)
