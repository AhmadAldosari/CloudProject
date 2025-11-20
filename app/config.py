"""Application configuration handling."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict
from urllib.parse import quote_plus


class ConfigError(RuntimeError):
    """Raised when mandatory configuration is missing."""


@dataclass
class Config:
    """Default configuration used in all environments."""

    SECRET_KEY: str = os.getenv("SECRET_KEY", "Admin123")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ENGINE_OPTIONS: Dict[str, Any] = None
    SQLALCHEMY_DATABASE_URI: str = None

    def __post_init__(self) -> None:
        self.SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
        self.SQLALCHEMY_DATABASE_URI = build_database_uri()


def build_database_uri() -> str:
    """Construct the MySQL connection string from environment variables."""
    host = os.getenv("DB_HOST","cloudprojectdb.cg3yo8ao4rxa.us-east-1.rds.amazonaws.com")
    user = os.getenv("DB_USER","admin")
    password = os.getenv("DB_PASS","Admin123")
    database = os.getenv("DB_NAME","cld_prj_db")
    port = os.getenv("DB_PORT", "3306")

    missing_vars = [
        name for name, value in [
            ("DB_HOST", host),
            ("DB_USER", user),
            ("DB_PASS", password),
            ("DB_NAME", database),
        ]
        if not value
    ]
    if missing_vars:
        joined = ", ".join(missing_vars)
        raise ConfigError(
            "Missing required database environment variables: " f"{joined}"
        )

    # Ensure credential parts are URL encoded in case of special characters.
    safe_user = quote_plus(user)
    safe_password = quote_plus(password)

    return f"mysql+pymysql://{safe_user}:{safe_password}@{host}:{port}/{database}"


def get_config() -> Config:
    """Return the default configuration object."""
    return Config()
