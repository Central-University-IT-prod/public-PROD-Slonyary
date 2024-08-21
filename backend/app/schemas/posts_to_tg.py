from app.schemas.base import BaseSchema


class PostsToTgChannelsCreate(BaseSchema):
    post_id: int
    channel_id: int
