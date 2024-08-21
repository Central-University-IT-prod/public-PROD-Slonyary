from app.schemas.base import BaseSchema


class UsersToTgChannelsCreate(BaseSchema):
    user_id: int
    channel_id: int
