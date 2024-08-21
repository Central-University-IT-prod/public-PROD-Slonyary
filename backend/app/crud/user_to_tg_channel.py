import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CrudBase
from app.schemas import TgChannelRead, TgChannelUpdate, UsersToTgChannelsCreate
from shared.database.models import TgChannel, User, UsersToTgChannels


class CrudUsersToTgChannels(
    CrudBase[
        UsersToTgChannels,
        UsersToTgChannelsCreate,
        TgChannelRead,
        TgChannelUpdate,
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db, UsersToTgChannels)

    async def is_user_access(self, user: User, tg_channel: TgChannel) -> bool:
        return bool(await self.get_relation(user.id, tg_channel.id))

    async def get_relation(
        self,
        tg_id: int,
        channel_id: int,
    ) -> UsersToTgChannels | None:
        query = sa.select(UsersToTgChannels).where(
            UsersToTgChannels.user_id == tg_id,
            UsersToTgChannels.channel_id == channel_id,
        )
        return await self.db.scalar(query)

    async def delete_relation(
        self,
        tg_id: int,
        channel_id: int,
    ) -> UsersToTgChannels | None:
        query = sa.select(UsersToTgChannels).where(
            UsersToTgChannels.user_id == tg_id,
            UsersToTgChannels.channel_id == channel_id,
        )
        result = await self.db.scalar(query)
        await self.db.delete(result)
        await self.db.commit()
        return
