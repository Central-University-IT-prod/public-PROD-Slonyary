from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.models.base import AlchemyBaseModel


class PostsToVkChannels(AlchemyBaseModel):
    __tablename__ = "posts_to_vk_channels"

    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="cascade"),
        primary_key=True,
    )
    channel_id: Mapped[int] = mapped_column(
        ForeignKey("vk_channels.id", ondelete="cascade"),
        primary_key=True,
    )
    message_id: Mapped[int] = mapped_column(Integer, nullable=True)
