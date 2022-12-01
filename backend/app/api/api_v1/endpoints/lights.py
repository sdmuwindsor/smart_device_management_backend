from typing import Any, List
from datetime import datetime
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.api import deps
from app.simulation import LightAnomaly
light_anamoly_obj = LightAnomaly.LightAnomalyDetection()
from app.utils.mail import send_mails

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


@router.get("/get_anamoly")
def get_anamoly(
    *,
    db: Session = Depends(deps.get_db),
    device_id: int
):
    light_anamoly_obj.detect_anomaly(device_id=device_id)
    details = db.query(models.Users.first_name, models.Users.email, models.Devices.name, models.Rooms.name).filter(
        models.Devices.id == device_id
    )
    print(details)
    # send_mails.send_report(details[0], details[1], light_anamoly_obj.pdf_file_path, details[2], details[3])