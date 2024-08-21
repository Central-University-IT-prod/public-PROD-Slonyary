import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.core.enums import PostStatus
from shared.database.models.base import AlchemyBaseModel

if TYPE_CHECKING:
    from shared.database.models.images import Image
    from shared.database.models.tg_channels import TgChannel
    from shared.database.models.users import User
    from shared.database.models.vk_channels import VkChannel


class Post(AlchemyBaseModel):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
    html_text: Mapped[str] = mapped_column(String(4096), nullable=False)
    plain_text: Mapped[str] = mapped_column(String(4096), nullable=False)
    publish_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    added_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now,
    )
    status: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default=PostStatus.moderation,
    )

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="created_posts",
        lazy="joined",
    )
    tg_channels: Mapped[list["TgChannel"]] = relationship(
        "TgChannel",
        secondary="posts_to_tg_channels",
        back_populates="posts",
        lazy="selectin",
    )
    vk_channels: Mapped[list["VkChannel"]] = relationship(
        "VkChannel",
        secondary="posts_to_vk_channels",
        back_populates="posts",
        lazy="selectin",
    )
    images: Mapped[list["Image"]] = relationship(
        "Image",
        back_populates="post",
        uselist=True,
        lazy="selectin",
        cascade="all,delete",
    )
