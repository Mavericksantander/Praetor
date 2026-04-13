from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PRAETOR_", env_file=None, extra="ignore")
    
    log_dir: Path = Path("data/logs")
    valid_classifications: list[str] = ["PUBLICA", "RESERVADO", "SECRETO"]


settings = Settings()
