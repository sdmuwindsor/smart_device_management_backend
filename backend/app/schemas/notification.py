from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class NotificationBase(BaseModel):
    user_id: int
    message: str
    title: datetime


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(NotificationBase):
    pass


class Notification(NotificationBase):
    id: int

    class Config:
        orm_mode = True

