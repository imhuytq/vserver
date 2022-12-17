from typing import Any, Dict, Optional
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_DATABASE: str
    DATABASE_DSN: Optional[PostgresDsn] = None

    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379

    @validator("DATABASE_DSN", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            path=f"/{values.get('DB_DATABASE') or ''}",
        )

    class Config:
        env_prefix = 'VSERVER_'
        case_sensitive = True


config = Settings()
