"""Vkontakte channel SQLAlchemy model."""

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database.models.base import AlchemyBaseModel

if TYPE_CHECKING:
    from shared.database.models.posts import Post
    from shared.database.models.users import User


class VkChannel(AlchemyBaseModel):
    __tablename__ = "vk_channels"

    id: Mapped[int] = mapped_column(BigInteger, unique=True, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
    title: Mapped[str] = mapped_column(String(64), nullable=False)
    access_token: Mapped[str] = mapped_column(String(512), nullable=False)
    added_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    description: Mapped[str] = mapped_column(String, nullable=True)
    photo_base64: Mapped[str] = mapped_column(String, nullable=True)

    owner: Mapped["User"] = relationship(
        "User",
        foreign_keys=owner_id,
        lazy="joined",
    )
    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="vk_channels",
        secondary="users_to_vk_channels",
        lazy="selectin",
    )
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        secondary="posts_to_vk_channels",
        back_populates="vk_channels",
        lazy="selectin",
    )
