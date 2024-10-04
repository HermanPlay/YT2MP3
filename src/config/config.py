from typing import Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


# Takes valus from environmental variables, or assigned ones.
class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")
    TOKEN: str
    POLLING: bool = False
    WEBHOOK_URL: Optional[str] = None
    ADMIN_ID: int = 0
    DB_PASSWORD: str
    DB_URI: Optional[str] = None
    SUPPORT_LINK: str = "@yt_mp3_support_bot"
    DEBUG: bool = False

    @model_validator(mode="before")
    @classmethod
    def assemble_db_uri(cls, data):
        if isinstance(data, dict):
            data[
                "DB_URI"
            ] = f"mongodb+srv://backend:{data.get('DB_PASSWORD')}@yt2mp3.3vaqogo.mongodb.net/?retryWrites=true&w=majority"
        return data


cfg = Config()
