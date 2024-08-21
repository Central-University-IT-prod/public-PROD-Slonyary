from app.schemas.base import BaseSchema


class UsersToVkChannelsCreate(BaseSchema):
    user_id: int
    channel_id: int
