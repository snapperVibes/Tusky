__all__ = ["settings", "security"]

import secrets
import unicodedata
import warnings
from datetime import datetime as DateTime, timedelta as TimeDelta
from typing import List, Optional, Dict, Any, Union

from passlib.context import CryptContext
from pydantic import BaseSettings, AnyHttpUrl, validator, EmailStr, PostgresDsn, HttpUrl

with warnings.catch_warnings():
    warnings.filterwarnings(
        "ignore", message=r"int_from_bytes is deprecated, use int\.from_bytes instead"
    )
    from jose import jwt


# # Todo: Figure out why these two lines are needed.
# #  It is directly related to CMD ["python" "manage.py" "initdb"] in backend.dockerfile
# import dotenv
#
# dotenv.load_dotenv("./.env.dev")


class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # Todo: Lower expire minutes for production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    SERVER_NAME: str
    # todo: SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:8080"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    SENTRY_DSN: Optional[HttpUrl] = None

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v

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

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    TEST_USER_NAME: str = "test_account"  # type: ignore
    FIRST_SUPERUSER: str = "Admin"  # type: ignore
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


class Security:
    ALGORITHM = "HS256"
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(
        self, subject: Union[str, Any], expires_delta: TimeDelta = None
    ) -> str:
        if expires_delta:
            expire = DateTime.utcnow() + expires_delta
        else:
            expire = DateTime.utcnow() + TimeDelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {"exp": expire, "sub": str(subject)}
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=self.ALGORITHM)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def to_identifier(self, text: str) -> str:
        """ Normalizes utf-8 strings using normalization form KD and lowercase characters """
        # https://unicode.org/reports/tr15/
        #   For each character, there are two normal forms: normal form C and normal form D.
        #   Normal form D (NFD) is also known as canonical decomposition,
        #   and translates each character into its decomposed form.
        #   Normal form C (NFC) first applies a canonical decomposition,
        #   then composes pre-combined characters again...
        #   The normal form KD (NFKD) will apply the compatibility decomposition,
        #   i.e. replace all compatibility characters with their equivalents.
        name = unicodedata.normalize("NFKD", text).lower()
        if "#" in name:
            raise
        return name


settings = Settings()
security = Security()
