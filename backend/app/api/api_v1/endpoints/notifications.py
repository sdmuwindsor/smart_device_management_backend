from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/get_user_notifications/{user_id}")
def get_user_notifications(
    user_id: int,
    db: Session = Depends(deps.get_db),
    # get_current_user: schemas.Room = Depends(deps.get_current_user)
):
    return crud.notification.get_by_user_id(db, user_id=user_id)
    