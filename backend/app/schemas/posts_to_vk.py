from pydantic import BaseModel


class PostsToVkChannelsCreate(BaseModel):
    post_id: int
    channel_id: int
