from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.models.base import AlchemyBaseModel


class UsersToVkChannels(AlchemyBaseModel):
    __tablename__ = "users_to_vk_channels"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"),
        primary_key=True,
    )
    channel_id: Mapped[int] = mapped_column(
        ForeignKey("vk_channels.id", ondelete="cascade"),
        primary_key=True,
    )
    role: Mapped[str] = mapped_column(String(64), nullable=False)
