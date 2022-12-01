from typing import Any, List
from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.core import security
# from app.utils import send_new_account_email

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
):
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.post("/login")
def login_access_token(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserLogin,
):
    user = crud.user.authenticate(
        db, email=user_in.username, password=user_in.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or passd")
    access_token_expires = timedelta(minutes=9600)
    access_token = {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
    return {**user.__dict__, **access_token}

@router.get("/get_power_consumption_by_date")
def get_power_consumption_by_date(
    *,
    db: Session = Depends(deps.get_db),
    start_date: datetime,
    end_date: datetime,
    user_id: int,
    category: str = None
    # get_current_user: schemas.Device = Depends(deps.get_current_user)

):
    power = crud.user.get_power_consumption_by_dates(
        db,
        start_date=start_date,
        end_date=end_date,
        user_id=user_id,
        category=category
    )
    return power


# @router.get("/test_login")
# def read_own_items(
#     current_user: schemas.User = Depends(deps.get_current_user)
# ):
#     return current_user
