from typing import Optional, Dict, Any
from pydantic import BaseSettings, HttpUrl, validator, parse_obj_as


# Takes valus from environmental variables, or assigned ones.
class Settings(BaseSettings):
    TOKEN: str
    POLLING: bool = False
    webhook_url: Optional[str] = None
    ADMIN_ID: int = 0
    DB_PASSWORD: str
    DB_URI: Optional[str] = None

    @validator("webhook_url", pre=True)
    def assemble_webhook_url(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return "https://yt2mp3-bot.herokuapp.com/" + values.get("TOKEN")
    
    @validator("DB_URI", pre=True)  
    def assemble_db_uri(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, cls):
            return v
        return f"mongodb+srv://backend:{values.get('DB_PASSWORD')}@yt2mp3.3vaqogo.mongodb.net/?retryWrites=true&w=majority"


settings = Settings()
