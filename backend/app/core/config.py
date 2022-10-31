import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn
from pydantic import validator


class Settings(BaseSettings):
    DB_HOST: str
    DB_PASSWORD: str
    DB_USER: str
    DB_NAME: str
    JWT_KEY: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
