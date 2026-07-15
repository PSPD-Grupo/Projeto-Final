from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    app_name: str = "patient-data-service"
    app_env: str = "development"

    grpc_host: str = "0.0.0.0"
    grpc_port: int = 50052
    http_host: str = "0.0.0.0"
    http_port: int = 8081

    db_host: str = Field(..., min_length=1)
    db_port: int = 5432
    db_name: str = Field(..., min_length=1)
    db_user: str = Field(..., min_length=1)
    db_password: str = Field(..., min_length=1)
    db_pool_min_size: int = 1
    db_pool_max_size: int = 10

    pseudonym_salt: str = "change-me-in-production"
    log_level: str = "INFO"

    jwt_secret: str = Field(..., min_length=1)

    model_config = SettingsConfigDict(env_file_encoding="utf-8")

    @property
    def database_dsn(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def grpc_bind_address(self) -> str:
        return f"{self.grpc_host}:{self.grpc_port}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
