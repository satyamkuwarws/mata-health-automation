from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        validate_assignment=True,
    )

    env: str = Field(default="local", alias="ENV")

    base_url: str = Field(default="https://nimble-pasca-24ee4c.netlify.app/admin", alias="BASE_URL")
    api_base_url: str | None = Field(default=None, alias="API_BASE_URL")

    # Defaults are intentionally non-secret placeholders. Override via `.env` or env vars.
    admin_username: str = Field(default="admin@example.com", alias="ADMIN_USERNAME")
    admin_password: str = Field(default="change-me", alias="ADMIN_PASSWORD")

    browser: Literal["chromium", "firefox", "webkit"] = Field(default="chromium", alias="BROWSER")
    headless: bool = Field(default=True, alias="HEADLESS")
    slow_mo_ms: int = Field(default=0, alias="SLOW_MO_MS")

    default_timeout_ms: int = Field(default=15_000, alias="DEFAULT_TIMEOUT_MS")
    expect_timeout_ms: int = Field(default=10_000, alias="EXPECT_TIMEOUT_MS")
    navigation_timeout_ms: int = Field(default=30_000, alias="NAVIGATION_TIMEOUT_MS")

    artifacts_dir: Path = Field(default=Path("reports/artifacts"), alias="ARTIFACTS_DIR")
    screenshots_dir: Path = Field(default=Path("reports/artifacts/screenshots"), alias="SCREENSHOTS_DIR")
    traces_dir: Path = Field(default=Path("reports/artifacts/traces"), alias="TRACES_DIR")
    videos_dir: Path = Field(default=Path("reports/artifacts/videos"), alias="VIDEOS_DIR")
    storage_state_dir: Path = Field(default=Path("reports/artifacts/storage"), alias="STORAGE_STATE_DIR")

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_dir: Path = Field(default=Path("reports/logs"), alias="LOG_DIR")

    def has_real_credentials(self) -> bool:
        return not (
            self.admin_username.strip().lower() in {"admin@example.com", "", "changeme", "change-me"}
            or self.admin_password.strip().lower() in {"changeme", "change-me", ""}
        )

    def ensure_dirs(self) -> None:
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.traces_dir.mkdir(parents=True, exist_ok=True)
        self.videos_dir.mkdir(parents=True, exist_ok=True)
        self.storage_state_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_dirs()
    return settings

