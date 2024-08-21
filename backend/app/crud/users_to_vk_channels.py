import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CrudBase
from app.schemas import TgChannelRead, TgChannelUpdate, UsersToVkChannelsCreate
from shared.database.models import User, UsersToVkChannels, VkChannel


class CrudUsersToVkChannels(
    CrudBase[
        UsersToVkChannels,
        UsersToVkChannelsCreate,
        TgChannelRead,
        TgChannelUpdate,
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db, UsersToVkChannels)

    async def is_user_access(self, user: User, vk_channel: VkChannel) -> bool:
        query = sa.select(UsersToVkChannels).where(
            UsersToVkChannels.user_id == user.id,
            UsersToVkChannels.channel_id == vk_channel.id,
        )
        result = await self.db.scalar(query)
        return bool(result)

    async def delete_relation(
        self,
        tg_id: int,
        channel_id: int,
    ) -> UsersToVkChannels | None:
        query = sa.select(UsersToVkChannels).where(
            UsersToVkChannels.user_id == tg_id,
            UsersToVkChannels.channel_id == channel_id,
        )
        result = await self.db.scalar(query)
        await self.db.delete(result)
        await self.db.commit()
        return
