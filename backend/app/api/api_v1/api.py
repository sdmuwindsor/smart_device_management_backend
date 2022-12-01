from fastapi import APIRouter

from app.api.api_v1.endpoints import users, rooms, devices, lights, thermostats, notifications

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(lights.router, prefix="/lights", tags=["lights"])
api_router.include_router(thermostats.router, prefix="/thermostats", tags=["thermostats"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
