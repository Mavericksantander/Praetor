from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PRAETOR_", env_file=None, extra="ignore")

    bitacora_dir: Path = Path("exports/bitacora")
    audit_log_path: Path = Path("data/audit.log")
    report_dir: Path = Path("exports/reports")


settings = Settings()
