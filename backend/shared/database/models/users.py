import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database.models.base import AlchemyBaseModel

if TYPE_CHECKING:
    from shared.database.models.posts import Post
    from shared.database.models.tg_channels import TgChannel
    from shared.database.models.vk_channels import VkChannel


class User(AlchemyBaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        unique=True,
        primary_key=True,
    )
    username: Mapped[int] = mapped_column(String(64), nullable=True)
    name: Mapped[str] = mapped_column(String(256), nullable=True)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)
    registered_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )

    created_posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="owner",
        lazy="selectin",
    )
    tg_channels: Mapped[list["TgChannel"]] = relationship(
        "TgChannel",
        secondary="users_to_tg_channels",
        back_populates="users",
        lazy="selectin",
    )
    vk_channels: Mapped[list["VkChannel"]] = relationship(
        "VkChannel",
        secondary="users_to_vk_channels",
        back_populates="users",
        lazy="selectin",
    )
