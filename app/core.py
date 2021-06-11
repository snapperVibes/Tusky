__all__ = ["settings", "security"]

import secrets
import warnings

from pydantic import BaseSettings, validator, PostgresDsn

with warnings.catch_warnings():
    warnings.filterwarnings(
        "ignore", message=r"int_from_bytes is deprecated, use int\.from_bytes instead"
    )
    from jose import jwt


class Settings(BaseSettings):
    API_STR_V1 = "/api/v1/"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
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
