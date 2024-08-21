from app.schemas.base import BaseSchema


class UserTelegramData(BaseSchema):
    id: int
    username: str | None = None
    auth_date: int
    first_name: str
    last_name: str | None = None
    hash: str
    photo_url: str | None


class UserCreate(BaseSchema):
    id: int
    username: str | None = None
    name: str
    photo_url: str | None


class UserUpdate(BaseSchema):
    photo_url: str


class UserRead(BaseSchema):
    id: int
    username: str | None = None
    name: str
