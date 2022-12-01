from typing import Any, List
from datetime import datetime
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/get_temperature_by_date")
def get_temperature_by_date(
    *,
    db: Session = Depends(deps.get_db),
    start_date: datetime,
    end_date: datetime,
    device_id: int,
    type: str
    # get_current_user: schemas.Device = Depends(deps.get_current_user)
):
    temperature = crud.thermostat.get_temperature_by_dates(
        db,
        start_date=start_date,
        end_date=end_date,
        device_id=int,
        type=str
    )
    print(temperature)
    return temperature


@router.get("/get_humidity_by_date")
def get_humidity_by_date(
    *,
    db: Session = Depends(deps.get_db),
    start_date: datetime,
    end_date: datetime,
    device_id: int,
    # get_current_user: schemas.Device = Depends(deps.get_current_user)
):
    humidity = crud.thermostat.get_humidity_by_dates(
        db,
        start_date=start_date,
        end_date=end_date,
        device_id=int,
    )
    print(humidity)
    return humidity


@router.get("/get_power_consumption_by_date")
def get_power_consumption_by_date(
    *,
    db: Session = Depends(deps.get_db),
    start_date: datetime,
    end_date: datetime,
    device_id: int,
    # get_current_user: schemas.Device = Depends(deps.get_current_user)
):
    power = crud.thermostat.get_power_consumption_by_dates(
        db,
        start_date=start_date,
        end_date=end_date,
        device_id=int,
    )
    print(power)
    return power
