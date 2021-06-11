__all__ = ["settings", "security"]

import secrets
import warnings
from typing import Optional, Dict, Any

from pydantic import BaseSettings, validator, PostgresDsn

with warnings.catch_warnings():
    warnings.filterwarnings(
        "ignore", message=r"int_from_bytes is deprecated, use int\.from_bytes instead"
    )
    from jose import jwt


class Settings(BaseSettings):
    API_STR_V1 = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "thalia"
    POSTGRES_PASSWORD: str = "changethis"
    POSTGRES_DB: str = "tusky"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True


class Security:
    pass

settings = Settings()
security = Security()
