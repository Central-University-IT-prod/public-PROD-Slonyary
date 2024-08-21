from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CrudBase
from app.schemas import VkChannelCreate, VkChannelRead, VkChannelUpdate
from shared.database.models import VkChannel


class CrudVkChannel(
    CrudBase[
        VkChannel,
        VkChannelCreate,
        VkChannelRead,
        VkChannelUpdate,
    ]
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, VkChannel)
