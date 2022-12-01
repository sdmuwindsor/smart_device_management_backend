from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Notifications
from app.schemas.notification import Notification, NotificationBase, NotificationCreate, NotificationUpdate


class CRUDNotification(CRUDBase[Notifications, NotificationCreate, NotificationUpdate]):
    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[Notifications]:
        return db.query(Notifications).filter(Notifications.user_id == user_id).all()
    


notification = CRUDNotification(Notifications)
