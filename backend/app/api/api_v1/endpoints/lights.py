from typing import Any, List
from datetime import datetime
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/get_brightness_by_date")
def get_brightness_by_date(
    *,
    db: Session = Depends(deps.get_db),
    start_date: datetime,
    end_date: datetime,
    device_id: int
    # get_current_user: schemas.Device = Depends(deps.get_current_user)

):
    lights = crud.light.get_by_dates(
        db,
        start_date=start_date,
        end_date=end_date,
        device_id=device_id
    )
    print(lights)
    return lights

@router.get("/get_power_consumption_by_date")
def get_power_consumption_by_date(
    *,
    db: Session = Depends(deps.get_db),
    start_date: datetime,
    end_date: datetime,
    device_id: int
    # get_current_user: schemas.Device = Depends(deps.get_current_user)

):
    lights = crud.light.get_by_dates(
        db,
        start_date=start_date,
        end_date=end_date,
        device_id=device_id
    )
    print(lights)
    return lights
