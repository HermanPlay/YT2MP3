from pydantic import BaseModel, Field


class User(BaseModel):
    username: str
    user_id: int
    first_name: str
    language_code: str
    active: bool = True
    admin: bool = False


class UserUpdate(BaseModel):
    username: str | None = Field(None, alias="username")
    first_name: str | None = Field(None, alias="first_name")
    active: bool | None = Field(None, alias="active")
