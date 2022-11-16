from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Room)
def create(
    *,
    db: Session = Depends(deps.get_db),
    room_in: schemas.RoomCreate,
    # get_current_user: schemas.Room = Depends(deps.get_current_user)

):
    room = crud.room.create(db, obj_in=room_in)
    return room

@router.put("/{id}", response_model=schemas.Room)
def update(
    *,
    id: int,
    db: Session = Depends(deps.get_db),
    room_in: schemas.RoomCreate,
    # get_current_user: schemas.Room = Depends(deps.get_current_user)

):
    room = crud.room.update(db, obj_in=room_in, id=id)
    return room


@router.get("/{id}")
def get(
    id: int,
    db: Session = Depends(deps.get_db),
    # get_current_user: schemas.Room = Depends(deps.get_current_user)
):
    return crud.room.get(db, id=id)


@router.get("/get_user_rooms/{user_id}")
def get_user_rooms(
    user_id: int,
    db: Session = Depends(deps.get_db),
    # get_current_user: schemas.Room = Depends(deps.get_current_user)
):
    return crud.room.get_by_user_id(db, user_id=user_id)
    