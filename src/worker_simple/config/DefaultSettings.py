import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    """Settings for APP."""

    activate_logging: bool = Field(alias="CUSTOM_LOGGING", default=False)

    app_version: str = Field(alias="APP_VERSION", default="dev")

    llm_call_url: str = Field(alias="LLM_CALL_URL", default="http://localhost:8056/api/v1")

    llm_call_timeout: str = Field(alias="LLM_CALL_TIMEOUT", default="180")


    temporal_server_url: str = Field(alias="TEMPORAL_SERVER_URL", default="http://localhost:7233")

    temporal_server_bearer: str = Field(alias="TEMPORAL_SERVER_BEARER", default="sssss")

    temporal_server_tls: bool = Field(alias="TEMPORAL_SERVER_TLS", default=False)

    def get_project_root(self) -> str:
        return Path(__file__).parent.parent.parent.as_posix() + os.path.sep
