from pathlib import Path

from pydantic import Field
from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict
from twitchAPI.type import AuthScope


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[".env.sample", ".env"], env_prefix="twitch_", case_sensitive=False
    )

    client_id: str = Field(default="...")
    client_secret: str = Field(default="...")
    target_channels: str = "jeens"
    user_scope: list[AuthScope] = [AuthScope.CHAT_READ]

    filtered_name: list[str] = ["gloria_bot", "nikmosi"]

    callback_url: Url = Url("http://localhost:8081/login/confirm")
    port: int = 8000

    storage_path: Path = Path("./var/token.json")
    heartbeat_path: Path = Path("./var/heartbeat")
    heartbeat_interval_seconds: float = 10.0
