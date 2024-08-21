from datetime import datetime

from pydantic import Field

from app.schemas import ImageRead
from app.schemas.base import BaseSchema, BaseSchemaPublishTime


class Channel(BaseSchema):
    id: int
    type: str


class ChannelRead(BaseSchema):
    id: int
    name: str
    avatar: str
    url: str
    type: str


class PostUpdate(BaseSchemaPublishTime):
    html_text: str | None = None
    plain_text: str | None = None
    publish_time: datetime | None = None


class PostIn(BaseSchemaPublishTime):
    html_text: str | None
    plain_text: str | None
    publish_time: datetime | None = None
    channels: list[Channel] = Field(default_factory=list)


class PostCreate(BaseSchemaPublishTime):
    html_text: str | None = None
    plain_text: str | None = None
    publish_time: datetime | None = None
    owner_id: int
    status: str


class PostChannel(BaseSchema):
    id: int
    name: str
    subscribers: int
    avatar: str | None = None
    type: str


class PreviewPost(BaseSchemaPublishTime):
    id: int
    status: str
    channels: list[PostChannel]
    publish_time: datetime | None = None
    owner_name: str
    photos: list[ImageRead]
    html_text: str | None = None
    plain_text: str | None = None
    views: int = 0
    reactions: int = 0
    shared: int = 0
    is_owner: bool


class PostRead(PreviewPost):
    owner_avatar: str
    publish_channels: list[ChannelRead]
