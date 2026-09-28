from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "EduGenie"
    app_version: str = "1.0.0"
    environment: str = "development"
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = True

    gemini_api_key: str = Field(default="", repr=False)
    gemini_model: str = "gemini-3.8-flash"

    explanation_provider: str = "gemini"
    local_explanation_enabled: bool = False
    local_explanation_model: str = "MBZUAI/LaMini-Flan-T5-783M"
    local_model_max_new_tokens: int = 256

    max_input_chars: int = 20000
    max_summary_chars: int = 30000
    max_quiz_chars: int = 20000
    max_learning_topic_chars: int = 500
    request_timeout_seconds: int = 90


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
